#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from typing import Mapping, Union

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersEnvironment,
)
from cmk.gui.valuespec import Dictionary, Float, Migrate, TextInput, Tuple


def _item_spec_siemens_plc_duration():
    return TextInput(
        title=_("Device Name and Value Ident"),
        help=_(
            "You need to concatenate the device name which is configured in the special agent "
            "for the PLC device separated by a space with the ident of the value which is also "
            "configured in the special agent."
        ),
    )


def migrate_duration_to_float(
    params: dict[str, tuple[Union[int, float], Union[int, float]]]
) -> Mapping[str, tuple[float, float]]:
    if params and "duration" in params:
        duration = params["duration"]
        params["duration"] = (float(duration[0]), float(duration[1]))

    return params


def _parameter_valuespec_siemens_plc_duration():
    return Migrate(
        Dictionary(
            elements=[
                (
                    "duration",
                    Tuple(
                        title=_("Duration"),
                        elements=[
                            Float(title=_("Warning at"), unit="s"),
                            Float(title=_("Critical at"), unit="s"),
                        ],
                    ),
                ),
            ],
            help=_(
                "This rule is used to configure thresholds for duration values read from "
                "Siemens PLC devices."
            ),
            title=_("Duration levels"),
        ),
        migrate=migrate_duration_to_float,
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="siemens_plc_duration",
        group=RulespecGroupCheckParametersEnvironment,
        item_spec=_item_spec_siemens_plc_duration,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_siemens_plc_duration,
        title=lambda: _("Siemens PLC Duration"),
    )
)
