# -*- coding: utf-8 *-*
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
