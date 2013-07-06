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


import numpy as np


def equalize_histogram(img, histogram, cfs):
    """
    Equalize pixel values to [0:255].
    """
    total_pixels = img.size
    N, M = img.shape
    min_value = img.min()
    L = 256  # Number of levels of grey
    cfs_min = cfs.min()
    img_corrected = np.zeros_like(img)
    corrected_values = np.zeros_like(histogram)

    divisor = np.float32(total_pixels) - np.float32(cfs_min)

    if not divisor:  # this happens when the image has all the values equals
        divisor = 1.0

    factor = (np.float32(L) - 1.0) / divisor

    corrected_values = ((np.float32(cfs) -
                         np.float32(cfs_min)) * factor).round()

    img_copy = np.uint64(img - min_value)
    img_corrected = corrected_values[img_copy]

    return img_corrected


def equalization_using_histogram(img):

    # Create histogram, bin edges and cumulative distributed function
    max_value = img.max()
    min_value = img.min()

    assert min_value >= 0, \
        "ERROR: equalization_using_histogram() img have negative values!"

    start, stop, step = int(min_value), int(max_value + 2), 1

    histogram, bin_edge = np.histogram(img, xrange(start, stop, step))
    cfs = histogram.cumsum()  # cumulative frencuency table
    img_corrected = equalize_histogram(img, histogram, cfs)

    return img_corrected


def naive_equalize_image(img, input_range, output_range):
    """
    Convert numbers in the img from input_range to output_range.
    Parameters:
        - img: numpy array
        - input_range: (old_min, old_max)
        - output_range (new_min, new_max)
    Return value:
        - A numpy array of the same dimensions of "img" with its contents
          range modified.
    """
    old_min, old_max = input_range
    new_min, new_max = output_range
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)

    assert old_max != 0, "ERROR: old_max cannot be zero."
    assert old_range > 0, "ERROR: old range negative difference."
    assert new_range > 0, "ERROR: new range negative difference."

    img_corrected = np.zeros_like(img)
    N, M = img.shape

    ###########################################################################
    # Convertion formula:
    #     old_range = (old_max - old_min)
    #     new_range = (new_max - new_min)
    #     new_value = (
    #                   (old_value - old_min) * (new_range/ old_range)
    #                 ) + new_min
    ###########################################################################
    factor = float(new_range) / float(old_range)

    img_corrected = np.int32(
                         (np.float32(img) - np.float32(old_min)) * \
                          factor + np.float32(new_min)
                        )

    return img_corrected
