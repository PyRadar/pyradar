=============
Tutorial (ES)
=============

Entendiendo los módulos de PyRadar
----------------------------------


- ``pyradar.core``

    Este módulo permite el manejo de imágenes SAR y además posee algoritmos
    para su ecualización.

    Las funciones que contiene este módulo son:

    - ``create_dataset_from_path(image_path)`` Desde el path de una imagen SAR,
      crea una estructura de datos, un dataset, para manejar su información.
      Esta estructura de datos, proviene de una librería externa llamada Gdal.

    - ``get_band_from_dataset(dataset)`` Obtiene la única banda de utilidad a
      nuestros fines del "dataset" pasado como argumento. Es importante notar
      que las imágenes que utilizamos poseen sólo una banda, dado que son
      imágenes de radar, en blanco y negro.

    - ``get_band_min_max(band)`` Retorna una tupla de Python con el máximo y
      mínimo de la banda "band".

    - ``read_image_from_band(band, xoff, yoff, win_xsize, win_ysize)`` Lee la
      banda convirtiéndola en un arreglo bidimensional(o matriz) de numpy,
      facilitando así el manejo de la información en un formato simple y más
      natural de manejar.

      Los parámetros significan lo siguiente:

        - *xoff* y *yoff*: indican con qué offset sobre el eje x y el eje y se deben leer los datos desde la imagen.
        - *win_xsize* y *win_ysize*: indican el tamaño de la ventana a leer de la imagen en largo y ancho.

    - ``get_geoinfo(dataset, cast_to_int)`` Esta función extrae la información
      de georreferenciación de un "dataset", con "cast_to_int" indicando si los
      datos de georreferenciación se encuentran como strings o como números
      crudos. De momento, no es utilizada por ninguno de los algoritmos, pero
      si en un futuro se quisiese extender PyRadar con funcionalidades que
      requieran el uso de georreferenciación, la base está preparada.

    - ``save_image(img_dest_dir, filename, img)`` Esta función se encarga de
      guardar una imagen "img" representada por un arreglo de numpy en le
      directorio *img_dest_dir* con nombre de archivo *filename*.

      Es importante destacar que *img* debe poseer valores en el rango
      *[0:255]* para que el procedimiento resulte exitoso. Si la imagen
      llegase a poseer valores fuera de este rango, se deberán normalizar los
      valores previamente utilizando los algoritmos de equalización provistos
      por este módulo.

    - ``equalization_using_histogram(img)`` Esta función normaliza los valores
      de *img* al rango *[0:255]*, utilizando como procedimiento intermedio
      *equalize_histogram*. Dicho algoritmo está basado en histogram_eq(img).

    - ``equalize_histogram(img, histogram, cfs)`` Dado el histograma y la
      función de distribución acumulada de *img*, este procedimiento normaliza
      los valores al rango *[0:255]*. Cabe notar que esta función es utilizada
      internamente por *equalization_using_histogram*.

    - ``naive_equalize_image(img, input_range, output_range)`` Esta función
      es una implementación sencilla y sin optimizaciones que sirve para
      normalizar imágenes desde el rango *input_range* al rango *output_range*.

    Ejemplo de uso:
    ---------------

    Este es el procedimiento estándar para abrir, leer y guardar una imagen SAR
    utilizando PyRadar. A continuación, en los ejemplos de los demás módulos,
    omitiremos estos pasos y haremos referencia a los mismos como
    "pasos básicos de lectura" desde los imports hasta (inclusive) la llamada
    del procedimiento "read_image_from_band". El siguiente ejemplo ilustra como
    utilizar "naive_equalize_image". Para ello se deben seguir los
    “*pasos básicos de lectura*”, y luego agregar el siguiente código:

    .. include:: ../../examples/example_core2.py
        :literal:

    Gdal es una librería para leer y escribir datos provenientes de rasters
    geoespaciales, y está liberada bajo licencia MIT por la Open Source
    Geospatial Foundation.

- ``filters``

    En este módulo se encuentran los siguientes filtros de ruido speckle:

    - Frost
    - Kuan
    - Lee
    - Lee Mejorado

    Los mismos siguen las definiciones matemáticas de la sección filtros.
    Además, se encuentran también las implementaciones de los filtros clásicos
    de media y de mediana. Como PyRadar tiene entre sus objetivos seguir
    expandiéndose y creciendo, este módulo puede ser extendido con nuevos
    filtros.

    Como complemento a estos algoritmos, se desarrolló una serie funciones
    que verifican la consistencia de los algoritmos en tiempo de ejecución.
    La finalidad de esto es que, al extender el módulo con nuevos filtros,
    el desarrollador no necesite escribir nuevo código para verificar estas
    condiciones en sus algoritmos para verificar consistencia.

    A continuación se detallan las funciones del módulo:

    - ``frost_filter(img, damping_factor, win_size)`` Esta función
      implementa el filtro de Frost sobre una imagen img, tomando como
      argumentos el damping_factor y el tamaño de ventana win_size. Si estos
      argumentos no fueran especificados, se toma por defecto:

        - damping_factor=2.0
        - win_size=3.

    - ``kuan_filter(img, win_size, cu)`` Esta función aplica el filtro de Kuan
      sobre una imagen img tomando como argumentos el tamaño de ventana win_size
      y coeficiente de variación del ruido cu. De no ser especificados los
      siguientes valores se toman por defecto: win_size=3 y cu=0.25

    - lee_filter(img, win_size, cu) Esta función aplica el filtro de Lee sobre
      una imagen img, tomando como argumentos el tamaño de ventana win_size y
      coeficiente de variación del ruido cu. De no ser especificados, se toman
      los mismos valores por defecto que en el filtro de Kuan.

    - lee_enhanced_filter(img, win_size, k, cu, cmax) Esta función aplica el
      filtro de Lee Mejorado con los siguientes argumentos:

        - la imagen img,
        - el tamaño win_size (por defecto 3),
        - k el factor de amortiguamiento (por defecto 1.0),
        - coeficiente de variación del ruido cu (por defecto 0.523),
        - coeficiente de variación máximo en la imagen cmax (por defecto 1.73).

    - ``mean_filter(img, win_size)`` Esta función ejecuta un filtro de paso bajo
          clásico, como lo es el filtro de media. Los argumentos que toma son
          la imagen img y el tamaño de la ventana win_size. Por defecto win_size toma el valor de 3.

    - ``median_filter(img, win_size)`` Esta función ejecuta el segundo filtro
      de paso bajo clásico que contiene el módulo: el filtro de mediana. Los
      argumentos de este filtro son la imagen img y el tamaño de ventana
      win_size, tomando por defecto 3 para este último.

    - Funciones desarrolladas para verificar consistencia de los filtros en tiempo de ejecución


    - ``assert_window_size(win_size)`` Verifica que el tamaño de ventana sea
      múltiplo de 3 y positivo. De no cumplirse la condición, levanta una excepción de Python.

    - ``assert_indices_in_range(width, height, xleft, xright, yup, ydown)`` Verifica
      que los índices de la ventana deslizante se encuentren dentro de los valores normales.

      Es decir, que siempre se cumpla lo siguiente: (0 <= xleft and xright <= width and 0 <= yup and ydown <= height)

      De no ser cierta la expresión booleana anterior, se levanta una excepción de Python.

    **Ejemplo de uso de los filtros:**

    Para correr los algoritmos de los filtros antes mencionados se necesitan
    ejecutar los "pasos básicos de lectura", para tener así la imagen img a usar en
    la variable “image”.

    .. include:: ../../examples/example_filtros.py
        :literal:

- ``pyradar.utils.timer`` un pequeño timer para cronometrar el tiempo de ejecución de porciones de código Python

  Se desarrolló este pequeño módulo con el fin de cronometrar el "tiempo de pared"
  de ejecución de algunas funciones. El tiempo de pared de ejecución es el tiempo
  total que un cálculo permanece en ejecución. Se le llama de "pared" porque
  dentro del sistema operativo la ejecución de un proceso también acarrea otra
  operaciones básicas además de la algoritmia programada. Operaciones como
  cambios de contexto del sistema operativo, carga y descarga de librerías,
  volcados de datos a disco y otras operaciones agregan tiempo extra a la
  medición. Si bien la medición no es de alta precisión, su valor es servir
  como medición de referencia de tiempo de ejecución para realizar optimizaciones.

    Ejemplos de uso:

    A diferencia de las demás utilidades antes mencionadas, esta utilidad la utilizamos dentro del código mismo.

    .. include:: ../../examples/example_timer.py
        :literal:

- ``pyradar.utils.sar_debugger``


    El propósito de este módulo de PyRadar es agrupar funcionalidades y
    herramientas para realizar tareas de debugging sobre algoritmos que manipulen
    imágenes SAR. De esta forma, el módulo irá satisfaciendo las necesidades de
    la comunidad con nuevos features. De momento sólo posee una función, take_snapshot().

    - ``takesnapshot(img)`` es una función que toma una fotografía instantánea
      de la imagen img y la guarda en el disco. El propósito de esta función,
      es poder exportar capturas de los algoritmos de clasificación a medida que
      van evolucionando en el cómputo.

    Ejemplo de uso:

    .. include:: ../../examples/example_sar_debugger.py
        :literal:

- ``pyradar.utils.system_info`` obtiene información del Sistema Operativo, Hardware y Software

  Se desarrolló un módulo que permite obtener información del Sistema Operativo
  de manera simple y detallada. El objetivo de este módulo es que cuando algún
  usuario o desarrollador tenga algún problema con la librería pyradar, éste
  pueda comparar la información específica sobre su Sistema Operativo, Hardware
  y Software, con el fin de descartar(o confirmar) la posibilidad de que su
  problema provenga de estas fuentes.

  Ejemplo de uso:

  .. include:: ../../examples/example_system_info.py
    :literal:

- ``pyradar.utils.statutils`` utilidades estadísticas

    Este módulo provee algunas funciones estadísticas que pueden llegar a ser
    de utilidad para la comunidad de procesamiento de imágenes, incluso más
    allá del contexto específico de la librería. Al igual que el módulo Sar
    Debugger, su objetivo también es ser extendido por la comunidad a medida
    que la necesidad lo demande.

    - ``compute_cfs()`` Recibiendo como argumento un histograma generado con la
      librería numpy, esta función genera una tabla con todas las frecuencias
      acumuladas.

    - ``calculate_pdf_for_pixel()`` Calcula la probabilidad de que un valor en
      particular aparezca en la imagen, donde la probabilidad está dada como:
      la cantidad de ocurrencias efectivas del valor * cantidad total de elementos.

    - ``calculate_cdf_for_pixel()`` Calcula el valor de un pixel en la función
      distribución acumulada.

    - ````compute_cdfs()`` Esta función computa todas la probabilidades de la
      distribución de frecuencia acumulada de cada valor en la imagen.

    Ejemplos de uso

    .. include:: ../../examples/example_statutils.py
        :literal:

- ``pyradar.classifiers.kmeans``

  Ejemplos de uso

  .. include:: ../../examples/example_kmeans.py
        :literal:

- ``pyradar.classifiers.isodata``

  Ejemplos de uso

  .. include:: ../../examples/example_isodata.py
        :literal:

  .. figure:: _static/isodata.gif
    :align: center
    :scale: 100 %

    Video in better quality: http://www.youtube.com/watch?v=4meidkmJWP0


- ``pyradar.simulate.image_simulator``

  Ejemplos de uso

  .. include:: ../../examples/example_simulate.py
    :literal:
