# -*- coding: utf-8 *-*
import os

from pyradar.core.sar import create_dataset_from_path
from pyradar.core.sar import get_band_from_dataset
from pyradar.core.sar import get_geoinfo
from pyradar.core.sar import read_image_from_band
from pyradar.core.sar import save_image

from pyradar.core.equalizers import equalization_using_histogram


from pyradar.filters.frost import frost_filter
from pyradar.filters.kuan import kuan_filter
from pyradar.filters.lee import lee_filter
from pyradar.filters.lee_enhanced import lee_enhanced_filter
from pyradar.filters.median import median_filter
from pyradar.filters.mean import mean_filter

from pyradar.utils.timeutils import Timer

from pyradar.classifiers.kmeans import kmeans_classification
from pyradar.classifiers.isodata import isodata_classification


try:
    ROOT = os.path.dirname(os.path.abspath(__file__.decode('utf-8')))
except:
    ROOT = "."

IMG_DEST_DIR = os.path.join(ROOT, 'Output')


if __name__ == '__main__':

    username = os.environ['USER']
    if username == 'carpincho':
        image_path = '/Users/carpincho/Dropbox/' \
                     'tesis/imagenes/SAR_ERS/SCENE1/DAT_01.001'
    elif username == 'matias':
        image_path = '/Volumes/Archivos/Dropbox/aa Tesis/'\
                     'imagenes/SAR_ERS/SCENE1/DAT_01.001'
    print username, image_path

    dataset = create_dataset_from_path(image_path)
    band = get_band_from_dataset(dataset)

    geoinfo = get_geoinfo(dataset, cast_to_int=True)

    xoff = geoinfo['xoff'] + 2000
    yoff = geoinfo['yoff'] + 2000

    ## Parameters:
    win_xsize = 6000  # window size in coord x
    win_ysize = 6000  # window size in coord y
    k = 1  # parameter of frost filter, ex: k=1 or k=10 or k=100
    win_size = 3  # size of the window for the filter function
    damping_factor = 1  # parameter of frost filter, ex: 1 or 10 or 1000

    image = read_image_from_band(band, xoff, yoff, win_xsize, win_ysize)

    # Try K-Means
#    kmean_timer = Timer()
#    n_classes = 8
#    iterations = 1000
#    class_image = kmeans_classification(image, n_classes, iterations)
#    kmean_timer.stop_timer()
#    kmean_timer.calculate_time_elapsed(print_value=True)

    # Try Isodata
    isodata_timer = Timer()
    parameters={"K": 8, "I":1000}
    class_image = isodata_classification(image,parameters=parameters )
    isodata_timer.stop_timer()
    isodata_timer.calculate_time_elapsed(print_value=True)
    numerito = parameters["K"]

    # Try the filters
#    filter_timer = Timer()
#    numerito = 11
#    cucito = 0.30
#    image_filtered = mean_filter(image, win_size=numerito)
#    image_filtered = median_filter(image,win_size)
#    image_filtered = frost_filter(image, damping_factor=1.0, win_size=11)
#    image_filtered = kuan_filter(image, win_size=7, cu=1.0)
#    image_filtered = lee_filter(image, win_size=numerito, cu=cucito)
#    image_filtered = lee_enhanced_filter(image, win_size=numerito, cu=cucito)
#    filter_timer.stop_timer()
#    diff = filter_timer.calculate_time_elapsed(print_value=True)

    # Frost y K-Means
#    ventana = 7
#    damp = 1.0
#
#    parameters={"K" : 5, "I" : 100}
#
#    _timer = Timer()
#
#    image_filtered = frost_filter(image, damping_factor=damp, win_size=ventana)
#    class_image = isodata_classification(image_filtered, parameters)
#
#
#    _timer.stop_timer()
#    _timer.calculate_time_elapsed(print_value=True)
#
#    image_corrected = equalization_using_histogram(class_image)
#    save_image(IMG_DEST_DIR, "image_" + str(ventana) + "frostisodata" +
#                str(damp) + "c"  + str(parameters["K"]), image_corrected)
#
#

    # Equalize and save the images to files
    image_corrected = equalization_using_histogram(class_image)
    save_image(IMG_DEST_DIR, "image_isodata8", image_corrected)
#
#    image_original = equalization_using_histogram(image)
#    save_image(IMG_DEST_DIR, "image_original", image_original)

    print "\a\a\a"
