# -*- coding: utf-8 -*-
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
