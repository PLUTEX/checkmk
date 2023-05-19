#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


import re
from collections.abc import Callable, Mapping

import cmk.base.plugins.agent_based.utils.sap_hana as sap_hana
from cmk.base.check_api import discover, get_parsed_item_data, LegacyCheckDefinition
from cmk.base.config import check_info

_SAP_HANA_CONNECT_STATE_MAP: Mapping[str, tuple[int, Callable[[str], bool]]] = {
    "Worker: OK": (0, lambda inp: inp == "0"),
    "Standby: OK": (0, lambda inp: inp == "1"),
    "No connect": (2, lambda inp: inp not in ("0", "1")),
}


def parse_sap_hana_connect(info):
    parsed: dict[str, dict] = {}
    for sid_instance, lines in sap_hana.parse_sap_hana(info).items():
        inst = parsed.setdefault(
            sid_instance,
            {
                "server_node": "not found",
                "driver_version": "not found",
                "timestamp": "not found",
                "cmk_state": 3,
                "message": " ".join(lines[0]),
            },
        )
        for elem in lines[0]:
            if "retcode" in elem:
                retcode = elem.split(":")[1].lstrip()
                for k, (state, evaluator) in _SAP_HANA_CONNECT_STATE_MAP.items():
                    if evaluator(retcode):
                        inst["cmk_state"] = state
                        inst["message"] = k
            if "Driver version" in elem:
                inst["driver_version"] = elem.split("Driver version")[1].lstrip()
            if "Connect string:" in elem:
                if (search := re.search("SERVERNODE=(.*?),(SERVERDB|UID|PWD)", elem)) is None:
                    raise ValueError(elem)
                inst["server_node"] = search.group(1)
            if "Select now()" in elem:
                if (search := re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", elem)) is None:
                    raise ValueError(elem)
                inst["timestamp"] = search.group()

    return parsed


@get_parsed_item_data
def check_sap_hana_connect(item, params, parsed):
    state = parsed["cmk_state"]
    message = "%s\nODBC Driver Version: %s, Server Node: %s, Timestamp: %s" % (
        parsed["message"],
        parsed["driver_version"],
        parsed["server_node"],
        parsed["timestamp"],
    )
    yield state, message


check_info["sap_hana_connect"] = LegacyCheckDefinition(
    parse_function=parse_sap_hana_connect,
    discovery_function=discover(),
    check_function=check_sap_hana_connect,
    service_name="SAP HANA CONNECT %s",
)
