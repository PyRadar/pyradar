# -*- coding: utf-8 *-*
import collections
import numpy as np

from scipy import optimize

from comparator_utils import RMSE, MAE, Pearson


class SimilarityMatrix(object):
    """
    Simple class to wrap, handle and return the matrix obtained as the
    result of comparing two images.
    """
    def __init__(self):
        pass


class ComparatorException(Exception):

    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class BaseImageComparator(object):

    def __init__(self, image_1, image_2):

        # perform input images validation
        self.validate_images_are_comparable(image_1, image_2)

        # initialize the instance attributes
        dimensions = image_1.shape
        (width, height) = dimensions
        self.dtype = image_1.dtype
        self.width = width
        self.height = height
        self.shape = (self.width, self.height)
        self.image1 = image_1
        self.image2 = image_2

    def validate_images_are_comparable(self, image1, image2):

        # assert images are both not none and of the required type
        if (image1 is None or image1 is None):
            msg = "WRONG IMAGES: images must be both not None to compare."
            raise ComparatorException(msg)

        if not (isinstance(image1, np.ndarray) and
                isinstance(image2, np.ndarray)):
            msg = "WRONG IMAGES: images must be numpy bi-dimensional arrays."
            raise ComparatorException(msg)

        # assert both images to have just one layer
        dimensions_img1 = image1.shape
        dimensions_img2 = image2.shape
        if not (len(dimensions_img1) == len(dimensions_img2) == 2):
            msg = "WRONG IMAGE DIMENSIONS: only images with one layer accepted."
            raise ComparatorException(msg)

        # assert the images to be of the same dimensions
        (width1, height1) = dimensions_img1
        (width2, height2) = dimensions_img2
        if (not (width1 == width2)):
            msg = "WRONG IMAGE DIMENSIONS: the width of the images differ.\n"\
                  "In order to be compared, both images must have the same "\
                  "dimensions(width and height)."
            raise ComparatorException(msg)

        if (not (height1 == height2)):
            msg = "WRONG IMAGE DIMENSIONS: the height of the images differ.\n"\
                  "In order to be compared, both images must have the same "\
                  "dimensions(width and height)."
            raise ComparatorException(msg)

        # assert both images contents to be of the same type
        dtype_img1 = image1.dtype
        dtype_img2 = image2.dtype

        if (not (dtype_img1 == dtype_img2)):
            msg = "IMAGE TYPES MISSMATCH: the dtype of the images differ.\n"\
                  "In order to be compared, both images must have the same "\
                  "dtype."
            raise ComparatorException(msg)

        # if no exception was raised up to this point, both images seem to be OK
        return True


class ImageComparator(BaseImageComparator):

    def __init__(self, image_1, image_2):
        super(ImageComparator, self).__init__(image_1, image_2)

    def calculate_rmse1(self):
        """ One way to compute RMSE. """
        x = self.image1.flatten()
        y = self.image2.flatten()

        rmse = RMSE()
        rmse.load(x, y)
        return rmse.compute()

    def calculate_rmse2(self):
        """ Another way to compute RMSE."""

        def calculate_residuals(p, x, y):
            return x - y

        x = self.image1.flatten()
        y = self.image2.flatten()

        Param = collections.namedtuple('Param', 'x0 y0 c k')
        p_guess = Param(x0=0, y0=0, c=0, k=0)

        p, cov, infodict, mesg, ier = optimize.leastsq(calculate_residuals,
                                                       p_guess,
                                                       args=(x, y),
                                                       full_output=1)
        p = Param(*p)

        # We could compute the residuals this way:
        # resid = residuals(p, x, y)
        # But we don't have to compute resid as infodict['fvec'] already
        # contains the info.
        resid = (infodict['fvec'])

        chisq = (resid ** 2).sum()
        dof = len(x) - len(p)  # "dof" is degrees of freedom
        rmse = np.sqrt(chisq / dof)
        return rmse

    def linspace_rmse(self, params):
        pass

    def calculate_mae(self):
        x = self.image1.flatten()
        y = self.image2.flatten()

        mae = MAE()
        mae.load(x, y)
        return mae.compute()

    def calculate_pearson(self):
        x = self.image1.flatten()
        y = self.image2.flatten()

        pearson = Pearson()
        pearson.load(x, y)
        return pearson.compute()

    def general_mean(self, params):
        pass

    def mean_matrix(self, params):
        pass

    def compare_by(self, strategy, params):
        """ Image comparison entry point. Performs the comparison of the
            images given in the initialization. """
        functions_dict = {
                'general_mean': '',
                'mean_matrix': '',
                'rmse1': self.calculate_rmse1,
                'rmse2': self.calculate_rmse2,
                'mae': self.calculate_mae,
                'pearson': self.calculate_pearson,
                }

        if strategy not in functions_dict.keys():
            raise ComparatorException("Strategy not available. "\
                            "Available strategies are: %s" % \
                            (", ".join(functions_dict.keys())), )

        f = functions_dict[strategy]
        if params:
            return f(params)
        else:
            return f()


if __name__ == '__main__':

    from pyradar.comparator.image_comparator import ImageComparator
    from pyradar.examples.sample_matrixes import (numpy_image,
                                                  numpy_image1)

    im = ImageComparator(numpy_image, numpy_image1)

    print 'rmse1: ', im.compare_by('rmse1', None)
    print 'rmse2: ', im.compare_by('rmse2', None)
    print 'mae: ', im.compare_by('mae', None)
    print 'pearson: ', im.compare_by('pearson', None)
