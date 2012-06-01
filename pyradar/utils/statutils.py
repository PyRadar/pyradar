# -*- coding: utf-8 *-*
import numpy as np


def compute_cfs(histogram):
    """
    Compute the cumulative frecuency table for the given np histogram.
    """
    cfs = np.zeros_like(histogram)
    partial_sum = 0

    start, stop, step = 0, histogram.size, 1
    for i in xrange(start, stop, step):
        partial_sum += histogram[i]
        cfs[i] = partial_sum

    return cfs


def calculate_pdf_for_pixel(image, histogram, bin_edge, value):
    """
    get the probability of 'value' appears in x with:
        P_x(i) = p(x=value) = ni / n

    where:
        x: is the image.
        ni: number of occurrences of 'value' in the image x.
        n: number of pixels of the image.
    """
    prob = 0.0
    n = image.size
    assert n > 0, 'ERROR:calculate_pdf_for_pixel() got and image size < 0.'

    result = np.where(bin_edge == value)[0]

    if result.size > 0:  # element in image
        index = result[0]
        prob = float(histogram[index]) / float(n)
    else:  # element does not exist
        pass

    return prob


def calculate_cdf_for_pixel(image, histogram, bin_edge, value):
    """
    \ cdf_x(i) = \sum_{j=0}^i p_x(j),
    """
    start, stop, step = 0, value + 1, 1
    acum = float(0)

    if bin_edge.max() < value:
        return float(1)

    for i in xrange(start, stop, step):
        acum += calculate_pdf_for_pixel(image, histogram, bin_edge, i)
        if acum == float(1):
            break

    return acum


def compute_cdfs(image, histogram, bin_edge):
    """
    Compute all the cdf values.
    Parameters:
            image: a np matrix representing the image.
            histogram: the histogram of the image.
    Returns:
            cdfs: an array with all the cdfs computed.
    """
    cdfs = np.zeros_like(histogram, float)

    max_value = image.max()
    min_value = image.min()
    start, stop, step = min_value, max_value + 1, 1

    for i in xrange(start, stop, step):
        local_pdf = calculate_pdf_for_pixel(image, histogram, bin_edge, i)
        index = i - min_value
        if i == start:
            cdfs[index] = local_pdf
        else:
            cdfs[index] = local_pdf + cdfs[index - 1]

    return cdfs
