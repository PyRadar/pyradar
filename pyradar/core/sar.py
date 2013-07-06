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


import os
from datetime import datetime

import Image
import numpy as np

from osgeo import gdal
from osgeo import gdalconst


def create_dataset_from_path(image_path):
    """
    Create dataset from image path and return the dataset.
    """
    mode = gdalconst.GA_ReadOnly
    dataset = gdal.Open(image_path, mode)

    assert bool(dataset), 'ERROR: gdal.Open retireved an invalid dataset.'

    # As we handle radar grayscale images, there's just one band.
    assert dataset.RasterCount == 1, 'ERROR: Image should have only one band.'

    return dataset


def get_band_from_dataset(dataset):
    """
    Get the band to work with from the dataset.
    There should be one *AND ONLY ONE* band in the dataset, as we only handle
    greyscale radar images.
    """
    assert bool(dataset), 'ERROR: get_band_from_dataset() from invalid dataset'

    # Choose the band to use (only 1 band)
    band_number = dataset.RasterCount

    assert band_number == 1, 'ERROR: more than one band in the dataset!'

    band = dataset.GetRasterBand(band_number)

    return band


def get_band_min_max(band):
    """
    If the band has min/max, just return it. If not, compute it and return it.
    """
    assert band, 'ERROR: band is invalid.'
    min = band.GetMinimum()
    max = band.GetMaximum()

    if min is None or max is None:
        (min, max) = band.ComputeRasterMinMax(1)

    return (min, max)


def read_image_from_band(band, xoff=0, yoff=0, win_xsize=None, win_ysize=None):
    """
    Internally using GDAL, get an image from band.
        xoff: x axis offset from where to start reading.
        yoff: y axis offset from where to start reading.
        win_xsize: x axis size of the windows to be read.
        win_ysize: y axis size of the windows to be read.

        Calling "read_image_from_band(band)" will read the whole image.
    """
    assert bool(band), 'ERROR: invalid band.'

    assert xoff >= 0, 'ERROR: xoff must be >= 0.'
    assert yoff >= 0, 'ERROR: yoff must be >= 0.'

    if win_xsize:
        assert win_xsize >= 0, 'ERROR: win_xsize must be >= 0.'
        x_overflow = band.XSize < xoff + win_xsize
        assert not x_overflow, \
            'ERROR: invalid parameters cause x window overflow.'

    if win_ysize:
        assert win_ysize >= 0, 'ERROR: win_ysize must be >= 0.'
        y_overflow = band.YSize < yoff + win_ysize
        assert not y_overflow, \
            'ERROR: invalid parameters cause y window overflow.'

    # the optimum way of reading an image is reading chunks of
    # band.GetBlocksize.
    img = band.ReadAsArray(xoff, yoff, win_xsize, win_ysize)

    return img


def get_geoinfo(dataset, cast_to_int=False):
    """
    Return a dictionary with the geoinfo of the dataset.
    """
    assert dataset, 'ERROR: invalid dataset.'
    base_geodata = dataset.GetGeoTransform()
    base_geodata = [int(x) for x in base_geodata] if cast_to_int \
                                                  else base_geodata
    geoinfo = {'xoff': base_geodata[0],
               'yoff': base_geodata[3],
               'xpixelsize': base_geodata[1],
               'ypixelsize': base_geodata[5]
                }

    return geoinfo


def save_image(img_dest_dir, filename, img):
    """
    Save an image with date and time as it filename.
    Parameters:
            img_dest_dir: the destination of the image.
            filename: a name for the file. With no extension.
            image: a numpy matrix that contains the image.
    """
    name = filename
    if not filename:
        # Create a unique name based on time:
        time_format = '%d%m%y_%H%M%S'
        time_today = datetime.today()
        name = time_today.strftime(time_format)

    supported_extensions = ['png', 'jpeg']
    extension = 'png'
    filename = name + '.' + extension

    assert extension in supported_extensions, "ERROR: save_image(). " \
                                              "format not valid."
    # Forge the path:
    img_dest_path = os.path.join(img_dest_dir, filename)

    # Convert the image from the numpy matrix using Image module:
    img_obj = Image.fromarray(img.astype(np.uint8))

    # And save it!
    img_obj.save(img_dest_path, extension)
    img_obj = None

    print 'File saved to "' + img_dest_path + '".'
