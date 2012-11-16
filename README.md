pyradar
=======

PyRadar official GIT repository.

## Módulos de PyRadar

### *core*, manejo de imágenes SAR y algoritmos de ecualización 

Este módulo permite el manejo de imágenes SAR y además posee algoritmos
para su ecualización.

(1,0)250

Las funciones que contiene este módulo son:

-   /create~d~ataset~f~rom~p~ath(image~p~ath)/ Desde el path de una
    imagen SAR, crea una estructura de datos, un *dataset*, para manejar
    su información. Esta estructura de datos, proviene de una librería
    externa llamada *Gdal*[^1].

-   /get~b~and~f~rom~d~ataset(dataset)/ Obtiene la única banda de
    utilidad a nuestros fines del “*dataset*” pasado como argumento. Es
    importante notar que las imágenes que utilizamos poseen sólo una
    banda, dado que son imágenes de radar, en blanco y negro.

-   /get~b~and~m~in~m~ax(band)/ Retorna una tupla de *Python* con el
    máximo y mínimo de la banda “*band*”.

-   /read~i~mage~f~rom~b~and(band, xoff, yoff, win~x~size, win~y~size)/
    Lee la banda convirtiéndola en un arreglo bidimensional(o *matriz*)
    de *numpy*, facilitando así el manejo de la información en un
    formato simple y más natural de manejar.

    Los parámetros significan lo siguiente:

    -   “*xoff*”, “*yoff*”, indican con qué *offset* sobre el eje $x$ y
        el eje $y$ se deben leer los datos desde la imagen,

    -   “*win\_xsize*”, “*win\_ysize*”, indican el tamaño de la ventana
        a leer de la imagen en *largo* y *ancho*.

-   /get~g~eoinfo(dataset, cast~t~o~i~nt)/ Esta función extrae la
    información de georreferenciación de un “*dataset*”, con
    “*cast\_to\_int*” indicando si los datos de georreferenciación se
    encuentran como *strings* o como *números crudos*.

    De momento, no es utilizada por ninguno de los algoritmos, pero si
    en un futuro se quisiese extender PyRadar con funcionalidades que
    requieran el uso de georreferenciación, la base está preparada.

-   /save~i~mage(img~d~est~d~ir, filename, img)/ Esta función se encarga
    de guardar una imagen “*img*” representada por un arreglo de *numpy*
    en le directorio \`‘*img\_dest\_dir’*’ con nombre de archivo
    “*filename*”.

    Es importante destacar que “*img*” debe poseer valores en el rango
    $[0:255]$ para que el procedimiento resulte exitoso. Si la imagen
    llegase a poseer valores fuera de este rango, se deberán normalizar
    los valores previamente utilizando los algoritmos de equalización
    provistos por este módulo.

-   /equalization~u~sing~h~istogram(img)/ Esta función normaliza los
    valores de “*img*” al rango $[0:255]$, utilizando como procedimiento
    intermedio “*equalize\_histogram*”. Dicho algoritmo está basado en
    \cite{histogram_eq}.

-   /equalize~h~istogram(img, histogram, cfs)/ Dado el histograma y la
    función de distribución acumulada de “*img*”, este procedimiento
    normaliza los valores al rango $[0:255]$. Cabe notar que esta
    función es utilizada internamente por
    “*equalization\_using\_histogram*”.

-   /naive~e~qualize~i~mage(img, input~r~ange, output~r~ange)/ Esta
    función es una implementación sencilla y sin optimizaciones que
    sirve para normalizar imágenes desde el rango “*input\_range*” al
    rango “*output\_range*”.

### Ejemplo de uso:

[source:pasosbasicosdelectura]

Este es el procedimiento estándar para *abrir*, *leer* y *guardar* una
imagen SAR utilizando PyRadar. A continuación, en los ejemplos de los
demás módulos, omitiremos estos pasos y haremos referencia a los mismos
como “*pasos básicos de lectura*” desde los *imports* hasta (inclusive)
la llamada del procedimiento “*read\_image\_from\_band*”. El siguiente
ejemplo ilustra como utilizar “*naive\_equalize\_image*”. Para ello se
deben seguir los “*pasos básicos de lectura*”, y luego agregar el
siguiente código:

capitulo4/pyradar~m~odules/example~c~ore2.py

[^1]: **Gdal** es una librería para leer y escribir datos provenientes
    de rasters geoespaciales, y está liberada bajo *licencia MIT* por la
    *Open Source Geospatial Foundation*.
