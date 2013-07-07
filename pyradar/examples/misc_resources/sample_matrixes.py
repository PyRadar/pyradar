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


# bi-dimensional
numpy_image = np.array([[52, 55, 61, 66, 70, 61, 64, 73],
                        [63, 59, 55, 90, 109, 85, 69, 72],
                        [62, 59, 68, 113, 144, 104, 66, 73],
                        [63, 58, 71, 122, 154, 106, 70, 69],
                        [67, 61, 68, 104, 126, 88, 68, 70],
                        [79, 65, 60, 70, 77, 68, 58, 75],
                        [85, 71, 64, 59, 55, 61, 65, 83],
                        [87, 79, 69, 68, 65, 76, 78, 94]])

# numpy_image1 = numpy_image * 2
numpy_image1 = np.array([[104, 110, 122, 132, 140, 122, 128, 146],
                         [126, 118, 110, 180, 218, 170, 138, 144],
                         [124, 118, 136, 226, 288, 208, 132, 146],
                         [126, 116, 142, 244, 308, 212, 140, 138],
                         [134, 122, 136, 208, 252, 176, 136, 140],
                         [158, 130, 120, 140, 154, 136, 116, 150],
                         [170, 142, 128, 118, 110, 122, 130, 166],
                         [174, 158, 138, 136, 130, 152, 156, 188]])

# tri-dimensional
numpy_image2 = np.array(
                    [
                        [
                            [52, 55, 61, 66],
                            [63, 59, 55, 90]
                        ],
                        [
                            [2, 5, 6, 6],
                            [6, 5, 5, 9]
                        ],
                        [
                            [2, 5, 1, 6],
                            [3, 9, 5, 0]
                        ]
                    ]
               )
