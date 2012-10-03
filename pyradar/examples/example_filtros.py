# -*- coding: utf-8 -*-
from pyradar.filters.frost import frost_filter
from pyradar.filters.kuan import kuan_filter
from pyradar.filters.lee import lee_filter
from pyradar.filters.lee_enhanced import lee_enhanced_filter
from pyradar.filters.median import median_filter
from pyradar.filters.mean import mean_filter

# filters parameters
# window size
winsize = 9
# damping factor for frost
k_value1 = 2.0
# damping factor for lee enhanced
k_value2 = 1.0
# coefficient of variation of noise
cu_value = 0.25
# coefficient of variation for lee enhanced of noise
cu_lee_enchanced = 0.523
# max coefficient of variation for lee enhanced
cmax_value = 1.73

# frost filter
image_frost = frost_filter(image, damping_factor=k_value1, win_size=winsize)
# kuan filter
image_kuan = kuan_filter(image, win_size=winsize, cu=cu_value)
# lee filter
image_lee = lee_filter(image, win_size=winsize, cu=cu_value)
# lee enhanced filter
image_lee_enhanced = lee_enhanced_filter(image, win_size=winsize, k=k_value2,
                                         cu=cu_lee_enchanced, cmax=cmax_value)
# mean filter
image_mean = mean_filter(image, win_size=winsize)
# median filter
image_median = median_filter(image, win_size=winsize)

