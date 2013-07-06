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
from matplotlib import pyplot, patches, path
#from matplotlib.ticker import FormatStrFormatter

fig = pyplot.figure()
ax = fig.add_subplot(111)

# histogram our data with np
data = np.random.randn(1000)
hist, bins = np.histogram(data, 100)


# get the corners of the rectangles for the histogram
left = np.array(bins[:-1])
right = np.array(bins[1:])
bottom = np.zeros(len(left))
top = bottom + hist
nrects = len(left)

# here comes the tricky part -- we have to set up the vertex and path
# codes arrays using moveto, lineto and closepoly

# for each rect: 1 for the MOVETO, 3 for the LINETO, 1 for the
# CLOSEPOLY; the vert for the closepoly is ignored but we still need
# it to keep the codes aligned with the vertices
nverts = nrects * (1 + 3 + 1)
verts = np.zeros((nverts, 2))
codes = np.ones(nverts, int) * path.Path.LINETO
codes[0::5] = path.Path.MOVETO
codes[4::5] = path.Path.CLOSEPOLY
verts[0::5, 0] = left
verts[0::5, 1] = bottom
verts[1::5, 0] = left
verts[1::5, 1] = top
verts[2::5, 0] = right
verts[2::5, 1] = top
verts[3::5, 0] = right
verts[3::5, 1] = bottom

barpath = path.Path(verts, codes)
patch = patches.PathPatch(barpath, facecolor='green', edgecolor='yellow',
                          alpha=0.5)
ax.add_patch(patch)

ax.set_xlim(left[0], right[-1])
ax.set_ylim(bottom.min(), top.max())

#ax.set_xticks(bins)
#ax.xaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

pyplot.show()


def draw_plot():
    import matplotlib.pyplot as plt
    import scipy.special as sps
    # Draw samples from the distribution:
    # Shape and scale(often refer as k and theta), both > 0
    shape, scale = 2., 2.  # mean and dispersion
    s = np.random.gamma(shape, scale, 1000)

    count, bins, ignored = plt.hist(s, 50, normed=True)
    y = bins ** (shape - 1) * (np.exp(-bins / scale) /
                          (sps.gamma(shape) * scale ** shape))

    # Display the histogram of the samples, along with
    # the probability density function:
    plt.plot(bins, y, linewidth=2, color='r')
    plt.show()
