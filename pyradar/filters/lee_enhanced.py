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


from math import exp

import numpy as np

from utils import assert_window_size
from utils import assert_indices_in_range

K_DEFAULT = 1.0
CU_DEFAULT = 0.523
CMAX_DEFAULT = 1.73


def weighting(pix_value, window, k=K_DEFAULT,
              cu=CU_DEFAULT, cmax=CMAX_DEFAULT):
    """
    Computes the weighthing function for Lee filter using cu as the noise
    coefficient.
    """

    # cu is the noise variation coefficient

    # ci is the variation coefficient in the window
    window_mean = window.mean()
    window_std = window.std()
    ci = window_std / window_mean

    if ci <= cu:  # use the mean value
        w_t = 1.0
    elif cu < ci < cmax:  # use the filter
        w_t = exp((-k * (ci - cu)) / (cmax - ci))
    elif ci >= cmax:  # preserve the original value
        w_t = 0.0

    return w_t


def assert_parameters(k, cu, cmax):
    """
    Asserts parameters in range.
    Parameters:
        - k: in [0:10]
        - cu: positive
        - cmax: positive and greater equal than cu
    """

    assert 0 <= k <= 10, \
        "k parameter out of range 0<= k <= 10, submitted %s" % k

    assert cu >= 0, \
        "cu can't be negative"

    assert cmax >= 0 and cmax >= cu, \
        "cmax must be positive and greater equal to cu: %s" % cu


def lee_enhanced_filter(img, win_size=3, k=K_DEFAULT, cu=CU_DEFAULT,
                        cmax=CMAX_DEFAULT):
    """
    Apply Enhanced Lee filter to a numpy matrix containing the image, with a
    window of win_size x win_size.
    """
    assert_window_size(win_size)
    assert_parameters(k, cu, cmax)

    # we process the entire img as float64 to avoid type overflow error
    img = np.float64(img)
    img_filtered = np.zeros_like(img)
    N, M = img.shape
    win_offset = win_size / 2

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

            pix_value = img[i, j]
            window = img[xleft:xright, yup:ydown]
            w_t = weighting(pix_value, window, k, cu, cmax)
            window_mean = window.mean()

            new_pix_value = (window_mean * w_t) + (pix_value * (1.0 - w_t))

            assert new_pix_value >= 0.0, \
                    "ERROR: lee_enhanced_filter(), pix " \
                    "filter can't be negative"

            img_filtered[i, j] = round(new_pix_value)

    return img_filtered
