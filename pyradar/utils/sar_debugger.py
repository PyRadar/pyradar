# -*- coding: utf-8 -*-
from pyradar.core.sar import save_image
from pyradar.core.equalizers import equalization_using_histogram


def take_snapshot(img, iteration_step=0):
    """
    Given image and iteration_step, saves 'image' concatenated with
    'iteration_step'.
    This function is ONLY for debug purposes.
    """
    folder_name = "./Output/"
    filename = "image_isodata" + "_" + str(iteration_step)

    img_eq = equalization_using_histogram(img)
    save_image(folder_name, filename, img_eq)
