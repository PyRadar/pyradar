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


from pyradar.comparator.image_comparator import ImageComparator
from pyradar.examples.sample_matrixes import (numpy_image,
                                              numpy_image1)

im = ImageComparator(numpy_image, numpy_image1)

print 'rmse1: ', im.compare_by('rmse1', None)
print 'rmse2: ', im.compare_by('rmse2', None)
print 'mae: ', im.compare_by('mae', None)
print 'pearson: ', im.compare_by('pearson', None)
