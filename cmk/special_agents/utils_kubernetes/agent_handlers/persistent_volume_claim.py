#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import itertools
from typing import Iterator, Mapping, Sequence

from cmk.special_agents.utils_kubernetes.schemata import api, section
from cmk.special_agents.utils_kubernetes.schemata.api import NamespaceName


def pod_attached_persistent_volume_claim_names(pod: api.Pod) -> Iterator[str]:
    if (volumes := pod.spec.volumes) is None:
        return

    for volume in volumes:
        if volume.persistent_volume_claim is None:
            continue

        yield volume.persistent_volume_claim.claim_name


def attached_pvc_names_from_pods(pods: Sequence[api.Pod]) -> Sequence[str]:
    return list(
        {pvc_name for pod in pods for pvc_name in pod_attached_persistent_volume_claim_names(pod)}
    )


def filter_kubelet_volume_metrics(
    kubelet_metrics: Sequence[api.OpenMetricSample],
) -> Iterator[api.KubeletVolumeMetricSample]:
    yield from (m for m in kubelet_metrics if isinstance(m, api.KubeletVolumeMetricSample))


def serialize_attached_volumes_from_kubelet_metrics(
    volume_metric_samples: Iterator[api.KubeletVolumeMetricSample],
) -> Iterator[section.AttachedVolume]:
    """Serialize attached volumes from kubelet metrics

    A PV can be bound to one PVC only, so while a PV itself has no namespace, the PVC
    namespace + name can be used to identify it uniquely (and easily)

    Remember: since a PVC has a namespace, only the namespace + name combination is unique
    """

    def pvc_unique(v: api.KubeletVolumeMetricSample) -> tuple[str, str]:
        return v.labels.namespace, v.labels.persistentvolumeclaim

    for (api_namespace, pvc), samples in itertools.groupby(
        sorted(volume_metric_samples, key=pvc_unique), key=pvc_unique
    ):
        volume_details = {sample.metric_name.value: sample.value for sample in samples}
        yield section.AttachedVolume(
            capacity=volume_details["kubelet_volume_stats_capacity_bytes"],
            free=volume_details["kubelet_volume_stats_available_bytes"],
            persistent_volume_claim=pvc,
            namespace=NamespaceName(api_namespace),
        )


def group_serialized_volumes_by_namespace(
    serialized_pvs: Iterator[section.AttachedVolume],
) -> Mapping[NamespaceName, Mapping[str, section.AttachedVolume]]:
    namespaced_grouped_pvs: dict[NamespaceName, dict[str, section.AttachedVolume]] = {}
    for pv in serialized_pvs:
        namespace_pvs: dict[str, section.AttachedVolume] = namespaced_grouped_pvs.setdefault(
            pv.namespace, {}
        )
        namespace_pvs[pv.persistent_volume_claim] = pv
    return namespaced_grouped_pvs


def group_parsed_pvcs_by_namespace(
    api_pvcs: Sequence[api.PersistentVolumeClaim],
) -> Mapping[NamespaceName, Mapping[str, section.PersistentVolumeClaim]]:
    namespace_sorted_pvcs: dict[NamespaceName, dict[str, section.PersistentVolumeClaim]] = {}
    for pvc in api_pvcs:
        namespace_pvcs: dict[str, section.PersistentVolumeClaim] = namespace_sorted_pvcs.setdefault(
            pvc.metadata.namespace, {}
        )
        namespace_pvcs[pvc.metadata.name] = section.PersistentVolumeClaim(
            metadata=section.PersistentVolumeClaimMetaData.parse_obj(pvc.metadata),
            status=section.PersistentVolumeClaimStatus.parse_obj(pvc.status),
            volume_name=pvc.spec.volume_name,
        )
    return namespace_sorted_pvcs
