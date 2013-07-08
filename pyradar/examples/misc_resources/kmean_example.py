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



import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
from scipy.cluster.vq import kmeans2
import pylab
pylab.close()

###############################################################################
__author__ = "Maciej Pacula"
__url__ = """http://blog.mpacula.com/2011/04/27/
           k-means-clustering-example-python/ """

# Adapted from
# http://hackmap.blogspot.com/2007/09/k-means-clustering-in-scipy.html
OUTPUT_FILE = "grap.png"
DIR = "."
IMG_PATH = os.path.join(DIR, OUTPUT_FILE)
K_CLASSES = 3
###############################################################################

# generate 3 sets of normally distributed points around
# different means with different variances
mu1, sigma1 = 1, 0.2
mu2, sigma2 = 2, 0.5
mu3, sigma3 = 3, 0.3
sample1 = np.random.normal(mu1, sigma1, (100, 2))
sample2 = np.random.normal(mu2, sigma2, (300, 2))
sample3 = np.random.normal(mu3, sigma3, (100, 2))

# slightly move samples 2 and 3 (for a prettier output)
sample2[:, 0] += 1
sample3[:, 0] -= 0.5

sets = np.concatenate((sample1, sample2, sample3))

sets = np.array(range(0,9))
print sets
###############################################################################
# kmeans for K_CLASSES clusters
#centroids, idx = kmeans2(np.array(zip(sets[:, 0], sets[:, 1])), K_CLASSES)
centroids, idx = kmeans2(sets.flatten(), K_CLASSES)
#centroids, idx = kmeans2(sets, K_CLASSES)
###############################################################################
green = [0.4, 1, 0.4]  # (102, 255, 102)
red = [1, 0.4, 0.4]  # (255, 102, 102)
light_blue = [0.1, 0.8, 1]  # (25, 204, 255)
colors = ([(green, red, light_blue)[i] for i in idx])

altoid = idx.reshape(3,3)
# plot colored points
#pylab.scatter(sets[:, 0], sets[:, 1], c=colors)
pylab.scatter(sets,sets, c=colors)

# mark centroids as (X)
point_size = 500
line_widths = 2
color_scheme = 'none'
circle_marker = 'o'
ex_marker = 'x'
#pylab.scatter(centroids[:, 0], centroids[:, 1], marker=circle_marker, \
#            s=point_size, linewidths=line_widths, c=color_scheme)
#pylab.scatter(centroids[:, 0], centroids[:, 1], marker=ex_marker, s=point_size,
#              linewidths=line_widths)

###############################################################################
# some tune
#pylab.title("Kmean Classification")  # title

#x_limits = (-1, 10)
#y_limits = (-1, 10)
#pylab.xlim(x_limits[0], x_limits[1])  # set ax x range
#pylab.ylim(y_limits[0], y_limits[1])  # set ax y range

pylab.grid(True)  # show grid

#pylab.annotate('this is the origin', xy=(0, 0), xytext=(4, -1), arrowprops=dict(facecolor='black', shrink=0.05))  # add a textmark
###############################################################################
# save image
pylab.savefig(IMG_PATH)

import ipdb; ipdb.set_trace()

