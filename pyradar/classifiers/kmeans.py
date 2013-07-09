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


from scipy.cluster.vq import vq
import numpy as np

# default number of clases
K_CLASSES = 5
# default number of iterations
ITER_MAX = 100


def initial_clusters(img_flat, k, method="random"):
    """Define initial clusters centers as startup.

    By default, the method is "linspace". Other method available is "random".

    """
    methods_availables = ["linspace", "random"]

    assert method in methods_availables, "ERROR: method %s is no valid." \
                                         "Methods availables %s" \
                                         % (method, methods_availables)
    if method == "linspace":
        max, min = img_flat.max(), img_flat.min()
        centers = np.linspace(min, max, k)
    elif method == "random":
        start, end = 0, img_flat.size
        indices = np.random.randint(start, end, k)
        centers = img_flat.take(indices)

    return centers


def update_centers(img_flat, img_class, centers):
    """Update the cluster center, computing the mean of all cluster members.

    """
    axis = 0
    n_clusters = centers.shape[0]
    for cluster in xrange(n_clusters):
        condition = np.equal(img_class, cluster)
        members = np.compress(condition, img_flat, axis)
        if members.shape[0] > 0:
            centers[cluster] = np.mean(members, axis)

    return centers


def converged_clusters(centers, last_centers, iter):
    """ Stop algorithm if there is no change in the clusters values between each
    iteration.

    Returns:
            - True if should stop, otherwise False.
    """
    return np.array_equiv(centers, last_centers)


def kmeans_classification(img, k=K_CLASSES, iter_max=ITER_MAX):
    """Classify a numpy 'image' according K-means algorithm.

    Parameters:
            - img: an input numpy array that contains the image to classify.
            - k: number of classes (if not setted will use 5 as default)
            - iter_max: maximum number of iterations (if not setted will use
              100 as default)

    Return value:
            - img_class: an numpy array image with the classification.

    """
    N, M = img.shape
    img_flat = img.flatten()

    centers = initial_clusters(img_flat, k, "linspace")

    for iter in xrange(0, iter_max):
        img_class, distances = vq(img_flat, centers)

        last_centers = centers.copy()
        centers = update_centers(img_flat, img_class, centers)

        if converged_clusters(centers, last_centers, iter):
            break

    print "Kmeans(info): Used %s classes." % k
    print "Kmeans(info): Number of Iterations done: %s." % (iter + 1)

    return img_class.reshape(N, M)
