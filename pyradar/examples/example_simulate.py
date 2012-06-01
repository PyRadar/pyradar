# -*- coding: utf-8 -*-
from pyradar.simulate.image_simulator import ImageSimulator
from pyradar.utils.timeutils import Timer
pylab.close()

timer = Timer()
width, height = 2000, 2000

gamma_ims = ImageSimulator(width, height)
k_ims = ImageSimulator(width, height)
noise_layer_ims = ImageSimulator(width, height)

gamma_params = {'scale': 2.0, 'shape': 3.0}
k_params = {'mean': 2.0, 'shape': 2.0}
noise_layer_params = {'df': 3}

gamma_ims.generate_image_layer(distribution='gamma', params=gamma_params)
k_ims.generate_image_layer(distribution='k', params=k_params)
noise_layer_ims.generate_noise_layer(distribution='chisquare', params=noise_layer_params)

# Make some noise!
gamma_ims.noise_layer = noise_layer_ims.noise_layer
k_ims.noise_layer = noise_layer_ims.noise_layer
gamma_ims.generate_noisy_layer()
k_ims.generate_noisy_layer()

timer.calculate_time_elapsed(print_value=True)
# Export the files:
gamma_ims.export_image_layer(layer_name='image_layer', filename='gamma_img_layer',
                             path_to='.')
k_ims.export_image_layer(layer_name='image_layer', filename='k_img_layer',
                         path_to='.')
gamma_ims.export_image_layer(layer_name='noisy_image', filename='gamma_noisy_img',
                             path_to='.')
k_ims.export_image_layer(layer_name='noisy_image', filename='k_noisy_img',
                         path_to='.')
timer.calculate_time_elapsed(print_value=True)

# Make a plot:
print 'Making a plot to "plot_img.png":'
pylab.close()
gamma_ims.plot_layer_histogram(layer_name='image_layer', filename='plot_gamma_img')
k_ims.plot_layer_histogram(layer_name='image_layer', filename='plot_k_img')

timer.stop_timer()
timer.calculate_time_elapsed(print_value=True)
