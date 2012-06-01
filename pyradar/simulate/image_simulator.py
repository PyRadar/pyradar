# -*- coding: utf-8 *-*
import numpy as np
import pylab

from pyradar.core.equalizers import equalization_using_histogram
from pyradar.core.sar import save_image

pylab.close()  # To shut pylab up.


class SimulatorException(Exception):

    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class ImageSimulator(object):
    """ Image simulator class.

        It bundles the stuff needed to generate simulations of real images,
        noise layers and the combination of those two into a noisy image.
        It also bundles the posibility to save a given layer to a file and
        to draw plots for the histogram of the layers.
        """
    def __init__(self, width, height):
        """ Initialize the matrixes for the layers with the given dimensions.
            'width' goes for columns, 'height' goes for rows. """
        dimensions = (width, height)
        self.dtype = np.uint16
        self.width = width
        self.height = height
        self.matrix_size = (self.width, self.height)

        self.image_layer = np.zeros(dimensions, self.dtype)
        self.noise_layer = np.zeros(dimensions, self.dtype)
        self.noisy_image = np.zeros(dimensions, self.dtype)

    def _generate_img_with_gama_dist(self, params):
        """FOR THE ORIGINAL IMAGE SIMULATION."""
        shape = params.get('shape', None)
        scale = params.get('scale', None)

        if (not (shape and scale)) or (shape <= 0) or (scale <= 0):
            msg = "Shape and scale are required parameters and must "\
                  "both be > 0."
            raise SimulatorException(msg)

        size = (self.width, self.height)
        self.image_layer = np.random.gamma(shape, scale, size)

    def _generate_img_with_k_dist(self, params):
        """
        FOR THE ORIGINAL IMAGE SIMULATION.
        K-distribution:
            Input:
                σ(mean): mean
                L: shape

            It is a product distribution: it is the distribution of the product
            of two independent random variables:

                A gamma distribution with Input:
                    1: mean
                    L(shape): shape

                A gamma distribution with input:
                    σ(mean): mean
                    ν: shape
        """
        shape = params.get('shape', None)
        mean = params.get('mean', None)

        if (not (shape and mean)) or (shape <= 0) or (mean <= 0):
            msg = "Shape and mean are required parameters and must "\
                  "both be > 0."
            raise SimulatorException(msg)

        size = self.matrix_size

        gamma1_mean = 1.0
        gamma1_shape = shape
        gamma1_scale = gamma1_mean / gamma1_shape
        gamma1_matrix = np.random.gamma(gamma1_shape, gamma1_scale, size)

        gamma2_mean = mean
        gamma2_shape = shape
        gamma2_scale = gamma2_mean / gamma2_shape
        gamma2_matrix = np.random.gamma(gamma2_shape, gamma2_scale, size)

        k_matrix = gamma1_matrix * gamma2_matrix
        self.image_layer = k_matrix

    def _generate_image_with_chisquare_dist(self, params):
        """ FOR THE NOISE LAYER.
            df : int
                Number of degrees of freedom.
        """
        df = params.get('df', None)

        if (not params) or (df <= 0):
            msg = "df parameter must be specified and must "\
                  "be > 0."
            raise self.SimulatorException(msg)

        self.noise_layer = np.random.chisquare(df, self.matrix_size)

    def generate_image_layer(self, distribution, params):
        """ Generate the -simulated- original image layer, without noise.
            Stores the result in self.image_layer.
            If distribution is 'gamma', params should be a dictionary with
            'shape' and 'scale' keys and values > 0 for both.
            If distribution is 'k', params should be a dictionary with 'df' key
            with a value > 0.
        """
        if distribution == 'gamma':
            self._generate_img_with_gama_dist(params)

        elif distribution == 'k':
            self._generate_img_with_k_dist(params)

        else:
            raise self.SimulatorException("Distribution not available.")

    def generate_noise_layer(self, distribution, params):
        """ Generate the -simulated- noise layer for the image.
            Stores the result in self.noise_layer. """
        if distribution == 'chisquare':
            self._generate_image_with_chisquare_dist(params)
        else:
            raise self.SimulatorException("Distribution not available.")

    def generate_noisy_layer(self):
        """ Combine the original - previously simulated- image layer with the
            -also previously simulated- noise layer.
            It is a precondition for this function for both images to be
            previously generated. If this is not the case, an exception will
            be raised. """

        if self.image_layer is None and \
           self.noise_layer is None:
            msg = u'Image layer and noise layer are both unset.'
            raise self.SimulatorException(msg)
        else:
            self.noisy_image = (self.image_layer * self.noise_layer)

    def _get_layer_securely(self, layer_name):
        available_layers = ['image_layer', 'noise_layer', 'noisy_image']
        if (not layer_name) or (layer_name not in available_layers):
            msg = 'Invalid layer name provided. Valid options are: %s. '\
                  'You provided: "%s".' % \
                                  (', '.join(available_layers), layer_name)
            raise self.SimulatorException(msg)

        map_dict = {
                'image_layer': self.image_layer,
                'noise_layer': self.noise_layer,
                'noisy_image': self.noisy_image
        }
        return map_dict[layer_name]

    def export_image_layer(self, layer_name, filename, path_to):
        """ Export an image file for a given layer to the given path. """

        layer = self._get_layer_securely(layer_name)
        img_matrix = equalization_using_histogram(layer)
        save_image(path_to, filename, img_matrix)

    def plot_layer_histogram(self, layer_name, filename):
        """ Draw a plot of the given layer.
        """
        layer = self._get_layer_securely(layer_name)

        # Calculate the histogram:
        histogram, bin_edges = pylab.histogram(layer, 50, normed=True)

        # Make a plot based on the histogram:
        pylab.plot(histogram)
        pylab.grid(True)
        pylab.title(layer_name.capitalize() + ' layer histogram plot.')
        pylab.savefig(filename)


if __name__ == '__main__':

    from pyradar.simulate.image_simulator import ImageSimulator
    from pyradar.utils.timeutils import Timer
    pylab.close()

    timer = Timer()
    width = 2000
    height = 2000

    gamma_ims = ImageSimulator(width, height)
    k_ims = ImageSimulator(width, height)
    noise_layer_ims = ImageSimulator(width, height)

    gamma_params = {'scale': 2.0, 'shape': 3.0}
    k_params = {'mean': 2.0, 'shape': 2.0}
    noise_layer_params = {'df': 3}

    gamma_ims.generate_image_layer(distribution='gamma', params=gamma_params)
    k_ims.generate_image_layer(distribution='k', params=k_params)
    noise_layer_ims.generate_noise_layer(distribution='chisquare',
                                         params=noise_layer_params)

    # Make some noise!
    gamma_ims.noise_layer = noise_layer_ims.noise_layer
    k_ims.noise_layer = noise_layer_ims.noise_layer
    gamma_ims.generate_noisy_layer()
    k_ims.generate_noisy_layer()

    timer.calculate_time_elapsed(print_value=True)

    # Export the files:
    gamma_ims.export_image_layer(layer_name='image_layer',
                                 filename='gamma_img_layer',
                                 path_to='.')
    k_ims.export_image_layer(layer_name='image_layer',
                             filename='k_img_layer',
                             path_to='.')
    gamma_ims.export_image_layer(layer_name='noisy_image',
                                 filename='gamma_noisy_img',
                                 path_to='.')
    k_ims.export_image_layer(layer_name='noisy_image',
                             filename='k_noisy_img',
                             path_to='.')

    timer.calculate_time_elapsed(print_value=True)

    # Make a plot:
    print 'Making a plot to "plot_img.png":'
    pylab.close()
    gamma_ims.plot_layer_histogram(layer_name='image_layer',
                                   filename='plot_gamma_img')
    k_ims.plot_layer_histogram(layer_name='image_layer',
                                   filename='plot_k_img')

    timer.stop_timer()
    timer.calculate_time_elapsed(print_value=True)
