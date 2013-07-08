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


from pyradar.core.sar import save_image
from pyradar.core.equalizers import equalization_using_histogram


def take_snapshot(img, iteration_step=0):
    """
    Given image and iteration_step, saves 'image' concatenated with
    'iteration_step'.
    This function is ONLY for debug purposes.
    """
    folder_name = "./Output/"
    filename = "image_isodata" + "_" + str(iteration_step)

    img_eq = equalization_using_histogram(img)
    save_image(folder_name, filename, img_eq)
