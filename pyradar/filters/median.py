# -*- coding: utf-8 *-*
import numpy as np

from utils import assert_window_size
from utils import assert_indices_in_range


def median_filter(img, win_size=3):
    """
    Apply a 'median filter' to 'img' with a window size equal to 'win_size'.
    Parameters:
        - img: a numpy matrix representing the image.
        - win_size: the size of the windows (by default 3)
    """

    assert_window_size(win_size)

    N, M = img.shape
    win_offset = win_size / 2
    img_filtered = np.zeros_like(img)

    for i in xrange(0, N):
        xleft = i - win_offset
        xright = i + win_offset

        if xleft < 0:
            xleft = 0
        if xright >= N:
            xright = N

        for j in xrange(0, M):
            yup = j - win_offset
            ydown = j + win_offset

            if yup < 0:
                yup = 0
            if ydown >= M:
                ydown = M

            assert_indices_in_range(N, M, xleft, xright, yup, ydown)

            window = img[xleft:xright, yup:ydown]
            window_median = np.median(window)

            img_filtered[i, j] = round(window_median)

    return img_filtered
