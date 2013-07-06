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


# this should be placed at the top with all the imports
from pyradar.classifiers.kmeans import kmeans_classification

# number of clusters
k= 4
# max number of iterations
iter_max = 1000
# run K-Means
class_image = kmeans_classification(image, k, iter_max)

# equalize class image to 0:255
class_image_eq = equalization_using_histogram(class_image)
# save it
save_image(IMG_DEST_DIR, "class_image_eq", class_image_eq)
# also save original image
image_eq = equalization_using_histogram(image)
# save it
save_image(IMG_DEST_DIR, "image_eq", image_eq)
