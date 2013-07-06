#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 - 2013
# Matías Herranz <matiasherranz@gmail.com>
# Joaquín Tita <joaquintita@gmail.com>
#
# hhttps://github.com/PyRadar/pyradar
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.


import platform
import pprint
import time


def get_system_info():
    """ Function to collect and display system information. """
    python_info = {
        'version': platform.python_version(),
        'version_tuple:': platform.python_version_tuple(),
        'compiler': platform.python_compiler(),
        'build': platform.python_build(),
    }

    platform_info = {
        'platform': platform.platform(aliased=True),
    }

    os_and_hardware_info = {
        'uname:': platform.uname(),
        'system': platform.system(),
        'node': platform.node(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
    }

    executable_architecture_info = {
        'interpreter': platform.architecture(),
        '/bin/ls': platform.architecture('/bin/ls')
    }

    info = {
        'python_info': python_info,
        'platform_info': platform_info,
        'os_and_hardware_info': os_and_hardware_info,
        'executable_architecture_info': executable_architecture_info,
    }

    return info


def print_info(info):
    """ The the tuple of info gathered by get_system_info and print
        it in a nice-for-the-human-eye fashion. """

    time_now = time.time()
    time_now_human = time.ctime(time_now)

    print "\nTime now: ", time_now
    print "Time now(for humans)", time_now_human

    pp = pprint.PrettyPrinter(depth=4)
    pp.pprint(info)


if __name__ == '__main__':
    """ main: print system info and exit. """
    info = get_system_info()
    print_info(info)
