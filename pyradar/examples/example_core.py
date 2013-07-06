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


from pyradar.core.sar import create_dataset_from_path
from pyradar.core.sar import get_band_from_dataset
from pyradar.core.sar import get_geoinfo
from pyradar.core.sar import read_image_from_band
from pyradar.core.sar import save_image

from pyradar.core.equalizers import equalization_using_histogram


IMAGE_PATH = "./img_sar/DAT_01.001"
IMG_DEST_DIR = "."

# create dataset
dataset = create_dataset_from_path(IMAGE_PATH)
# get band from dataset
band = get_band_from_dataset(dataset)
# get geo info from dataset
geoinfo = get_geoinfo(dataset, cast_to_int=True)

#usually both values are zero
xoff = geoinfo['xoff']
yoff = geoinfo['yoff']

# window size in coord x
win_xsize = 128
# window size in coord y
win_ysize = 128

image = read_image_from_band(band, xoff, yoff, win_xsize, win_ysize)

#equalize img to 0:255
image_eq = equalization_using_histogram(image)
# save img in current directory
save_image(IMG_DEST_DIR, "image_sar", image_eq)
