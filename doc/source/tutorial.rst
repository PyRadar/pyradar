========
Tutorial
========

Understanding PyRadar's modules
-------------------------------


- ``pyradar.core``

    This module deals with SAR images and also contains equalization
    algorithms.

    This module contains the following functions:

    - ``create_dataset_from_path(image_path)`` from the path to a SAR
      image, it creates a data structure (a dataset) to manage the
      image's information. This data structure is defined in an
      external library (Gdal).

    - ``get_band_from_dataset(dataset)`` extracts the only usable band
      (for our purposes) from the dataset passed as parameter. NB: we
      are dealing only with images which can contain only one band, as
      radar images are black and white.

    - ``get_band_min_max(band)`` returns a Python tuple with the
      maximum and minimum values for the band passed as parameter.

    - ``read_image_from_band(band, xoff, yoff, win_xsize, win_ysize)``
      reads the band into numpy's bidirectional array (or matrix), a
      simpler and more natural format.

      The meaning of the different parameters is as follows:

        - *xoff* and *yoff*: offset over the x and y axis where the
          image data should start being read.

        - *win_xsize* y *win_ysize*: window size in height and width.

    - ``get_geoinfo(dataset, cast_to_int)`` extract the georeferencing
      information from the dataset. "cast_to_int" implies whether the
      georeferencing data are represented as strings or raw
      numbers. For the time being, it is not employed by any of the
      other algorithms, but it could be useful to extend PyRadar with
      georeferencing functionality.

    - ``save_image(img_dest_dir, filename, img)`` saves an image in
      numpy array format to the folder *img_dest_dir* with file name
      *filename*.

      NB: *img* should have values in the range *[0:255]*. Outside
      that range, the values should be normalized using the
      equalization algorithms in the same module.

    - ``equalization_using_histogram(img)`` normalizes the values in
      *img* to the range *[0:255]*, using the function
      *equalize_histogram* (which in turn uses histogram_eq(img)).

    - ``equalize_histogram(img, histogram, cfs)`` given both the
      histogram and CDF for *img*, normalize its values to the range
      *[0:255]* (using *equalization_using_histogram*).

    - ``naive_equalize_image(img, input_range, output_range)`` a
      simple and straightforward normalization from range
      *input_range* to the range *output_range*.

    Example of use:
    ---------------

    This the standard procedure for opening, reading and saving a SAR
    image using PyRadar. In the remainder examples, we will omit these
    steps and we will refer to them as "basic reading steps", from the
    imports until the call to the function "read_image_from_band"
    (inclusive). The following example shows how to use
    "naive_equalize_image". We should follow the *basic reading steps*
    and then add the following piece of code:

    .. include:: ../../examples/example_core2.py
        :literal:

    Gdal is a library to read and write geospatial raster data and it
    distributed under MIT license by the Open Source Geospatial
    Foundation.

- ``filters``

    This module contains the speckle noise filters:

    - Frost
    - Kuan
    - Lee
    - Improved Lee

    They follow the mathematical models described in the filters
    section.  Besides these, there are also implementations of the
    classic mean and median filters. This module can be easily
    expanded with new filters.

    Besides the algorithms, there are a series of functions that help
    verify the correctness of the algorithms at run time. This should
    simplify testing new filters.

    Module functions:

    - ``frost_filter(img, damping_factor, win_size)`` implementation
      of Frost filtering over the image img, taking as parameters the
      damping_factor and the window size win_size. Default values:

        - damping_factor=2.0
        - win_size=3.

    - ``kuan_filter(img, win_size, cu)`` apply the Kuan filter to an
      image img, taking as parameters the window size win_size and the
      noise variation rate cu. Default values: win_size=3 y cu=0.25

    - lee_filter(img, win_size, cu) apply the Lee filter to an image
      img, taking as parameters as image img, taking as parameters the
      window size win_size and the noise variation rate cu. Default
      values: win_size=3 y cu=0.25

    - lee_enhanced_filter(img, win_size, k, cu, cmax) applies the 
      Improved Lee filter with the following parameters:

        - the image img,
        - the window size win_size (default: 3),
        - the dumping factor k (default: 1.0),
        - image maximum variation coefficient cmax (default: 1.73).

    - ``mean_filter(img, win_size)`` applies a traditional lo pass
      filter (the mean filter). It takes as parameters the image img
      and the window size win_size. The default value of win_size
      is 3.

    - ``median_filter(img, win_size)`` applies another traditional lo
      pass filter (the median filter). It takes as parameters the
      image img and the window size win_size. The default value of
      win_size is 3.

    - Test harness functions


    - ``assert_window_size(win_size)`` verifies the windows size is a
      multiple of 3 and positive, otherwise it raises a Python
      exception.

    - ``assert_indices_in_range(width, height, xleft, xright, yup,
      ydown)`` verifies the indices of the sliding window fall into
      expected values.

      That it, the following invariant should hold: (0 <= xleft and xright <= width and 0 <= yup and ydown <= height)

      If it does not hold, it raises a Python exception.

    **Example usage for the filters:**

    After executing the "basic reading steps", the image to be used
    for filtering should available in the variable “image”.

    .. include:: ../../examples/example_filtros.py
        :literal:

- ``pyradar.utils.timer`` a small timer to profile Python execution time

  A small module to profile the "wall time" of the execution of some
  functions.  Wall time is the time a particular function is
  executing, and it includes Operating System overhead. Even though is
  not very precise, it is useful as reference to measure the impact of
  different optimizations.

    Example of use:

    This utility is used within the code itself.

    .. include:: ../../examples/example_timer.py
        :literal:

- ``pyradar.utils.sar_debugger``


    This module groups debugging tools for algorithms that manipulate
    SAR images. Over time, it should grow but currently it has only
    one function, take_snapshot().

    - ``takesnapshot(img)`` take a snapshot of the image img and saves
      it to disk. It can be used to capture intermediate stages of the
      classification algorithms.

    Example of use:

    .. include:: ../../examples/example_sar_debugger.py
        :literal:

- ``pyradar.utils.system_info`` obtains information about the
  Operating System, Hardware and Software

  This module allows for obtaining detailed Operating System
  information in a simple way.  It is used for error reporting, to
  diagnose Operating System-related issues.

  Example of use:

  .. include:: ../../examples/example_system_info.py
    :literal:

- ``pyradar.utils.statutils`` statistical utilities

    This module contains statistical utilities of general interest to
    the image processing community. In the same way as SAR Debugger,
    this module can be easily extended as needed.

    - ``compute_cfs()`` takes as parameter a histogram produced by
      numpy, it produces a table with all the accumulated frequencies.

    - ``calculate_pdf_for_pixel()`` compute the probability of a
      particular value appearing in the image, where the probability
      is given by the amount of actual times the value appears * total
      number of elements.

    - ``calculate_cdf_for_pixel()`` compute the value of a pixel in
      the cumulative distribution function.

    - ````compute_cdfs()`` computes the cumulative distribution
      frequency for each value in the image.

    Example of use

    .. include:: ../../examples/example_statutils.py
        :literal:

- ``pyradar.classifiers.kmeans``

  Example of use

  .. include:: ../../examples/example_kmeans.py
        :literal:

- ``pyradar.classifiers.isodata``

  Example of use

  .. include:: ../../examples/example_isodata.py
        :literal:

  .. figure:: _static/isodata.gif
    :align: center
    :scale: 100 %

    Video in better quality: http://www.youtube.com/watch?v=4meidkmJWP0


- ``pyradar.simulate.image_simulator``

  Example of use

  .. include:: ../../examples/example_simulate.py
    :literal:
