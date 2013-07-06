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


import os, shutil, zipfile, unittest

from pyradar.core.sar import create_dataset_from_path
from pyradar.core.sar import get_band_from_dataset
from pyradar.core.sar import get_geoinfo
from pyradar.core.sar import read_image_from_band
from pyradar.core.sar import save_image

from pyradar.core.equalizers import equalization_using_histogram


from pyradar.filters.frost import frost_filter
from pyradar.filters.kuan import kuan_filter
from pyradar.filters.lee import lee_filter
from pyradar.filters.lee_enhanced import lee_enhanced_filter
from pyradar.filters.median import median_filter
from pyradar.filters.mean import mean_filter

from pyradar.utils.timeutils import Timer

from pyradar.classifiers.kmeans import kmeans_classification
from pyradar.classifiers.isodata import isodata_classification


#===============================================================================
# CONSTANTS
#===============================================================================

try:
    ROOT = os.path.dirname(os.path.abspath(__file__.decode('utf-8')))
except:
    ROOT = "."

TEST_ZIPS = os.path.join(ROOT, 'testpkg')

IMAGES = os.path.join(ROOT, "_test_images")

IMG_DEST_DIR = os.path.join(ROOT, '_test_output')

TEMP_DIR_DISCLAIMER = os.path.join(IMG_DEST_DIR, "warning.txt")


#===============================================================================
# PREPARE DIRS
#===============================================================================

if os.path.exists(IMG_DEST_DIR):
    shutil.rmtree(IMG_DEST_DIR)
os.mkdir(IMG_DEST_DIR)
with open(TEMP_DIR_DISCLAIMER, "w") as fp:
    fp.write("WARNING:\n\t THIS FOLDER IS DETROYED IN EVERY TEST")


if not os.path.exists(IMAGES):
    import sys
    print "Extracting files to zips, It's only the first time"
    print "please wait..."
    for dname, _, fnames in os.walk(TEST_ZIPS):
        for fname in fnames:
            fpath = os.path.join(dname, fname)
            with zipfile.ZipFile(fpath, "r") as z:
                z.extractall(IMAGES)


#===============================================================================
# TESTS
#===============================================================================

class TestAll(unittest.TestCase):

    def test_all(self):
        image_path = os.path.join(IMAGES,  "DAT_01.001")

        print image_path

        dataset = create_dataset_from_path(image_path)
        band = get_band_from_dataset(dataset)

        geoinfo = get_geoinfo(dataset, cast_to_int=True)

        xoff = geoinfo['xoff'] + 2000
        yoff = geoinfo['yoff'] + 2000

        ## Parameters:
        win_xsize = 100  # window size in coord x
        win_ysize = 100  # window size in coord y
        k = 1  # parameter of frost filter, ex: k=1 or k=10 or k=100
        win_size = 3  # size of the window for the filter function
        damping_factor = 1  # parameter of frost filter, ex: 1 or 10 or 1000

        image = read_image_from_band(band, xoff, yoff, win_xsize, win_ysize)

        # Try K-Means
        kmean_timer = Timer()
        n_classes = 8
        iterations = 1000
        class_image = kmeans_classification(image, n_classes, iterations)
        kmean_timer.stop_timer()
        kmean_timer.calculate_time_elapsed(print_value=True)

        # Try Isodata
        isodata_timer = Timer()
        parameters={"K": 8, "I":1000}
        class_image = isodata_classification(image,parameters=parameters )
        isodata_timer.stop_timer()
        isodata_timer.calculate_time_elapsed(print_value=True)
        numerito = parameters["K"]

        # Try the filters
        filter_timer = Timer()
        numerito = 11
        cucito = 0.30
        image_filtered = mean_filter(image, win_size=numerito)
        image_filtered = median_filter(image,win_size)
        image_filtered = frost_filter(image, damping_factor=1.0, win_size=11)
        image_filtered = kuan_filter(image, win_size=7, cu=1.0)
        image_filtered = lee_filter(image, win_size=numerito, cu=cucito)
        image_filtered = lee_enhanced_filter(image, win_size=numerito, cu=cucito)
        filter_timer.stop_timer()
        diff = filter_timer.calculate_time_elapsed(print_value=True)

        # Frost y K-Means
        ventana = 7
        damp = 1.0
    #
        parameters={"K" : 5, "I" : 100}
    #
        _timer = Timer()
    #
        image_filtered = frost_filter(image, damping_factor=damp, win_size=ventana)
        class_image = isodata_classification(image_filtered, parameters)
    #
    #
        _timer.stop_timer()
        _timer.calculate_time_elapsed(print_value=True)
    #
        image_corrected = equalization_using_histogram(class_image)
        save_image(IMG_DEST_DIR, "image_" + str(ventana) + "frostisodata" +
                    str(damp) + "c"  + str(parameters["K"]), image_corrected)
    #
    #

        # Equalize and save the images to files
        image_corrected = equalization_using_histogram(class_image)
        save_image(IMG_DEST_DIR, "image_isodata8", image_corrected)
    #
        image_original = equalization_using_histogram(image)
        save_image(IMG_DEST_DIR, "image_original", image_original)

        print "\a\a\a"


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)

