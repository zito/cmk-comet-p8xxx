#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:sta:si:sw=4:sts=4:et:

# Check has been developed using:
# P8510 - Thermometer with Ethernet interface,
#         internal temperature sensor
# Device Firmware Version	P8510 sensor Firmware Version 4-5-1.16
#
# +------------------------------------------------------------------+
# | This file has been contributed by:                               |
# |                                                                  |
# | Václav Ovsík <vaclav.ovsik@gmail.com>             Copyright 2019 |
# +------------------------------------------------------------------+

# Example info:
#   [['Channel 1',
#     '19.9',
#     'Channel 2',
#     'error 1',
#     'Channel 3',
#     'error 1',
#     'Channel 4',
#     'error 1']]
#

from collections.abc import Mapping

from .agent_based_api.v1.type_defs import CheckResult, DiscoveryResult, StringTable
from .agent_based_api.v1 import (
    OIDEnd,
    Result,
    SNMPTree,
    Service,
    State,
    equals,
    get_value_store,
    register,
)

from .utils.temperature import check_temperature, TempParamType

Section = Mapping[str, float]


def parse_comet_p8xxx(string_table: StringTable) -> Section:
    kv = string_table[0]
    section = {}
    for chname, chval in zip(kv[::2], kv[1::2]):
        try:
            id = chname.replace('Channel ', '')
            section[id] = float(chval)
        except:
            pass
    return section

register.snmp_section(
    name="comet_p8xxx",
    detect=equals(
        ".1.3.6.1.2.1.1.2.0",
        ".1.3.6.1.4.1.1723.2.1.2",
    ),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.22626.1.5.2",
        oids=[
            "1.1",    # P8510-MIB::ch1Name
            "1.2",    # P8510-MIB::ch1Val
            "2.1",    # P8510-MIB::ch2Name      badly designed MIB :(
            "2.2",    # P8510-MIB::ch2Val       so we support
            "3.1",    # P8510-MIB::ch3Name      up to 4 channels
            "3.2",    # P8510-MIB::ch3Val       only
            "4.1",    # P8510-MIB::ch4Name
            "4.2",    # P8510-MIB::ch4Val
        ],
    ),
    parse_function=parse_comet_p8xxx,
)

def inventory_comet_p8xxx(section: Section) -> DiscoveryResult:
    for item, value in section.items():
        yield Service(item=item)

def check_comet_p8xxx(
    item: str,
    params: TempParamType,
    section: Section,
) -> CheckResult:
    if item in section:
        yield from check_temperature(reading=section[item],
                                 params=params,
                                 unique_name=f"comet_p8xxx_{item}",
                                 value_store=get_value_store(),
                                 dev_unit='c')
    else:
        yield Result(state=State.UNKNOWN, summary="Item not found")


register.check_plugin(
    name="comet_p8xxx",
    service_name="Sensor %s",
    discovery_function=inventory_comet_p8xxx,
    check_function=check_comet_p8xxx,
    check_ruleset_name="temperature",
    check_default_parameters={},
)
