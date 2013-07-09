#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyradar.comparator.image_comparator import ImageComparator
from pyradar.examples.sample_matrixes import (numpy_image,
                                              numpy_image1)

im = ImageComparator(numpy_image, numpy_image1)

print 'rmse1: ', im.compare_by('rmse1', None)
print 'rmse2: ', im.compare_by('rmse2', None)
print 'mae: ', im.compare_by('mae', None)
print 'pearson: ', im.compare_by('pearson', None)
