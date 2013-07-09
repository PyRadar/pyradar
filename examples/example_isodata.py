#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this should be placed at the top with all the imports
from pyradar.classifiers.isodata import isodata_classification

params = {"K": 15, "I" : 100, "P" : 2, "THETA_M" : 10, "THETA_S" : 0.1,
          "THETA_C" : 2, "THETA_O" : 0.01}

# run Isodata
class_image = isodata_classification(img, parameters=params)

# equalize class image to 0:255
class_image_eq = equalization_using_histogram(class_image)
# save it
save_image(IMG_DEST_DIR, "class_image_eq", class_image_eq)
# also save original image
image_eq = equalization_using_histogram(image)
# save it
save_image(IMG_DEST_DIR, "image_eq", image_eq)
