# -*- coding: utf-8 -*-
# get actual range
input_range = image.min(), image.max()
# set new range
output_range = 0, 255
# equalize image
image_eq = naive_equalize_image(image, input_range, output_range)
# save image in current directory
save_image(IMG_DEST_DIR, "image_sar", image_eq)
