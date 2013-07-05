#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 - 2013
# Matias Herranz <matiasherranz@gmail.com>
# Joaquin Tita <joaquintita@gmail.com>
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


from pyradar.filters.frost import frost_filter
from pyradar.filters.kuan import kuan_filter
from pyradar.filters.lee import lee_filter
from pyradar.filters.lee_enhanced import lee_enhanced_filter
from pyradar.filters.median import median_filter
from pyradar.filters.mean import mean_filter

# filters parameters
# window size
winsize = 9
# damping factor for frost
k_value1 = 2.0
# damping factor for lee enhanced
k_value2 = 1.0
# coefficient of variation of noise
cu_value = 0.25
# coefficient of variation for lee enhanced of noise
cu_lee_enhanced = 0.523
# max coefficient of variation for lee enhanced
cmax_value = 1.73

# frost filter
image_frost = frost_filter(image, damping_factor=k_value1, win_size=winsize)
# kuan filter
image_kuan = kuan_filter(image, win_size=winsize, cu=cu_value)
# lee filter
image_lee = lee_filter(image, win_size=winsize, cu=cu_value)
# lee enhanced filter
image_lee_enhanced = lee_enhanced_filter(image, win_size=winsize, k=k_value2,
                                         cu=cu_lee_enhanced, cmax=cmax_value)
# mean filter
image_mean = mean_filter(image, win_size=winsize)
# median filter
image_median = median_filter(image, win_size=winsize)

