#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 - 2013
# Matías Herranz <matiasherranz@gmail.com>
# Joaquín Tita <joaquintita@gmail.com>
#
# https://github.com/PyRadar/pyradar
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


#===============================================================================
# DOCS
#===============================================================================

"""This file is for distribute pyradar with setuptools

"""


#===============================================================================
# IMPORTS
#===============================================================================

import sys

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

import pyradar


#===============================================================================
# CONSTANTS
#===============================================================================

PYPI_REQUIRE = [
    "pillow",
    "numpy",
    "matplotlib",
    "scipy"
]

MANUAL_REQUIRE = {
    "gdal" : "http://gdal.org/",
}


# sugerido pero no importante
SUGESTED = {

}


#===============================================================================
# WARNINGS FOR MANUAL REQUIRES AND SUGGESTED
#===============================================================================

def validate_modules(requires):
    not_found = []
    for name, url in requires.items():
        try:
            __import__(name)
        except ImportError:
            not_found.append("{} requires '{}' ({})".format(pyradar.PRJ,
                                                             name, url))
    return not_found

def print_not_found(not_found, msg):
    limits = "=" * max(map(len, not_found))
    print("\n{}\n{}\n{}\n{}\n".format(msg, limits,
                                        "\n".join(not_found),
                                        limits))

not_found = validate_modules(MANUAL_REQUIRE)
if not_found:
    print_not_found(not_found, "ERROR")
    sys.exit(1)


not_found = validate_modules(SUGESTED)
if not_found:
    print_not_found(not_found, "WARNING")


#===============================================================================
# FUNCTIONS
#===============================================================================

setup(
    name=pyradar.PRJ.lower(),
    version=pyradar.STR_VERSION,
    description=pyradar.SHORT_DESCRIPTION,
    author=pyradar.AUTHOR,
    author_email=pyradar.EMAIL,
    url=pyradar.URL,
    license=pyradar.LICENSE,
    keywords=pyradar.KEYWORDS,
    classifiers=pyradar.CLASSIFIERS,
    packages=[pkg for pkg in find_packages() if pkg.startswith("pyradar")],
    include_package_data=True,
    package_data={
        'ExampleImages': ['pyradar/simulate/ExampleImages/*'],
        'DemoSet' : ['pyradar/simulate/DemoSet/*'],
    },
    py_modules=["ez_setup"],
    install_requires=PYPI_REQUIRE,
)
