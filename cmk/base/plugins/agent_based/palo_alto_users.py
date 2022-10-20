#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from dataclasses import dataclass
from typing import Mapping, Optional

from .agent_based_api.v1 import (
    check_levels,
    Metric,
    register,
    render,
    Result,
    Service,
    SNMPTree,
    State,
)
from .agent_based_api.v1.type_defs import CheckResult, DiscoveryResult, StringTable
from .utils.palo_alto import DETECT_PALO_ALTO


@dataclass(frozen=True)
class Section:
    num_users: int
    max_users: int


def parse(string_table: StringTable) -> Section | None:
    return (
        Section(num_users=int(string_table[0][1]), max_users=int(string_table[0][0]))
        if string_table
        else None
    )


register.snmp_section(
    name="palo_alto_users",
    parse_function=parse,
    detect=DETECT_PALO_ALTO,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.25461.2.1.2.5.1",
        oids=[
            "2.0",  # panGPGWUtilizationMaxTunnels
            "3.0",  # panGPGWUtilizationActiveTunnels
        ],
    ),
)


def discover(section: Section) -> DiscoveryResult:
    yield Service()


def check(section: Section) -> CheckResult:
    user_perc = section.num_users / section.max_users * 100

    yield Result(
        state=State.OK,
        summary=f"Number of logged in users: "
        f"{render.percent(user_perc)} - {section.num_users} of {section.max_users}",
    )

    yield from check_levels(
        section.num_users,
        metric_name="num_user",
        render_func=str,
        label="Absolute number of users",
        notice_only=True,
    )
    yield from check_levels(
        user_perc,
        render_func=render.percent,
        label="Relative number of users",
        notice_only=True,
    )

    yield Metric("max_user", section.max_users)


def cluster_check(section: Mapping[str, Optional[Section]]) -> CheckResult:
    yield from check(
        Section(
            num_users=sum(
                (node_section.num_users if node_section else 0 for node_section in section.values())
            ),
            max_users=sum(
                (node_section.max_users if node_section else 0 for node_section in section.values())
            ),
        ),
    )


register.check_plugin(
    name="palo_alto_users",
    service_name="Palo Alto Users",
    discovery_function=discover,
    check_function=check,
    cluster_check_function=cluster_check,
)
