#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# vim:sta:si:sw=4:sts=4:et:
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2012             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# The Check_MK official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# Check has been developed using:
# P8510 - Thermometer with Ethernet interface,
#         internal temperature sensor
# Device Firmware Version	P8510 sensor Firmware Version 4-5-1.16
#
# +------------------------------------------------------------------+
# | This file has been contributed by:                               |
# |                                                                  |
# | Václav Ovsík <vaclav.ovsik@gmail.com>             Copyright 2012 |
# +------------------------------------------------------------------+


def perfometer_check_mk_comet_p8xxx(row, check_command, perf_data):
    info = row["service_plugin_output"]
    temp = float(perf_data[0][1])
    color = '#00ff00'
    if info.startswith('WARN'):
        color = '#ffff00'
    if info.startswith('CRIT'):
        color = '#ff0000'
    return (str(temp) + '°C'), perfometer_logarithmic(temp, 21, 1.2, color)

perfometers['check_mk-comet_p8xxx'] = perfometer_check_mk_comet_p8xxx
