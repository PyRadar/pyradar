# -*- coding: utf-8 -*-
import numpy as np
from pyradar.utils.statutils import compute_cfs
from pyradar.utils.statutils import calculate_pdf_for_pixel
from pyradar.utils.statutils import calculate_cdf_for_pixel
from pyradar.utils.statutils import compute_cdfs
arr = np.array([31, 49, 19, 62, 24, 45, 23, 51, 55, 60, 40, 35,
                54, 26, 57, 37, 43, 65, 18, 41, 50, 56, 4, 54,
                39, 52, 35, 51, 63, 42])
max_value = arr.max()
min_value = arr.min()
start, stop, step = int(min_value), int(max_value + 2), 1

histogram, bin_edge = np.histogram(arr, xrange(start, stop, step)
compute_cfs(histogram)
>>> array([ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
            1,  2,  3,  3, 3,  3,  4,  5,  5,  6,  6,  6,  6,
            6,  7,  7,  7,  7,  9,  9, 10, 10, 11, 12, 13, 14,
           15, 15, 16, 16, 16, 16, 17, 18, 20, 21, 21, 23, 24,
           25, 26, 26, 26, 27, 27, 28, 29, 29, 30])

calculate_pdf_for_pixel(arr, histogram, bin_edge, 54)
>>> 0.066666666666666666
calculate_pdf_for_pixel(arr, histogram, bin_edge, 20)
>>> 0.0
calculate_pdf_for_pixel(arr, histogram, bin_edge, 18)
>>> 0.033333333333333333

calculate_cdf_for_pixel(arr, histogram, bin_edge, 4)
>>> 0.033333333333333333
calculate_cdf_for_pixel(arr, histogram, bin_edge, 50)
>>> 0.59999999999999998

compute_cdfs(arr, histogram, bin_edge)
>>> array([ 0.03333333,  0.03333333,  0.03333333,  0.03333333,  0.03333333,
            0.03333333,  0.03333333,  0.03333333,  0.03333333,  0.03333333,
            0.03333333,  0.03333333,  0.03333333,  0.03333333,  0.06666667,
            0.1       ,  0.1       ,  0.1       ,  0.1       ,  0.13333333,
            0.16666667,  0.16666667,  0.2       ,  0.2       ,  0.2       ,
            0.2       ,  0.2       ,  0.23333333,  0.23333333,  0.23333333,
            0.23333333,  0.3       ,  0.3       ,  0.33333333,  0.33333333,
            0.36666667,  0.4       ,  0.43333333,  0.46666667,  0.5       ,
            0.5       ,  0.53333333,  0.53333333,  0.53333333,  0.53333333,
            0.56666667,  0.6       ,  0.66666667,  0.7       ,  0.7       ,
            0.76666667,  0.8       ,  0.83333333,  0.86666667,  0.86666667,
            0.86666667,  0.9       ,  0.9       ,  0.93333333,  0.96666667,
            0.96666667,  1.        ])
