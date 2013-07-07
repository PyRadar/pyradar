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

from utils import assert_window_size
from utils import assert_indices_in_range


def mean_filter(img, win_size=3):
    """
    Apply a 'mean filter' to 'img' with a window size equal to 'win_size'.
    Parameters:
        - img: a numpy matrix representing the image.
        - win_size: the size of the windows (by default 3).
    """
    assert_window_size(win_size)

    N, M = img.shape
    win_offset = win_size / 2
    img_filtered = np.zeros_like(img)

    for i in xrange(0, N):
        xleft = i - win_offset
        xright = i + win_offset

        if xleft < 0:
            xleft = 0
        if xright >= N:
            xright = N

        for j in xrange(0, M):
            yup = j - win_offset
            ydown = j + win_offset

            if yup < 0:
                yup = 0
            if ydown >= M:
                ydown = M

            assert_indices_in_range(N, M, xleft, xright, yup, ydown)

            window = img[xleft:xright, yup:ydown]
            window_mean = window.mean()

            img_filtered[i, j] = round(window_mean)

    return img_filtered
