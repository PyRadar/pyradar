# -*- coding: utf-8 -*-
from osgeo import gdal
#from osgeo import osr
#from osgeo import ogr
from osgeo import gdalconst
#from osgeo import gdal_array
import struct
abs_path = "/Users/carpincho/Dropbox/tesis/imagenes/SAR_ERS/SCENE1/DAT_01.001"


def get_fmt_string(format, count):
    """
    See http://docs.python.org/library/struct.html#format-characters
    """
    formats = {'float': 'f', }  # we can add more types here. Read the docs.

    # Assert we know this format:
    assert format in formats.keys(), 'ERROR: format unknown'

    # Assert 'count' is a positive integer:
    assert isinstance(count, int), 'ERROR: count is not an integer'
    assert count > 0, 'ERROR: count must be a positive integer'

    return formats[format] * count


dataset = gdal.Open(abs_path, gdalconst.GA_ReadOnly)
print '\n'

#######Getting dataset information#############################################
print 'Driver: ', dataset.GetDriver().ShortName, \
        '/', dataset.GetDriver().LongName
print 'Size is ', dataset.RasterXSize, 'x', dataset.RasterYSize,\
        'x', dataset.RasterCount
print 'Projection is ', dataset.GetProjection()

geotransform = dataset.GetGeoTransform()
if not geotransform is None:
        print 'Origin = (', geotransform[0], ',', geotransform[3], ')'
        print 'Pixel Size = (', geotransform[1], ',', geotransform[5], ')'

######Fetching a Raster Band###################################################
print '\n'

band = dataset.GetRasterBand(1)
print 'Band Type', gdal.GetDataTypeName(band.DataType)
min = band.GetMinimum()
max = band.GetMaximum()

if min is None or max is None:
    (min, max) = band.ComputeRasterMinMax(1)
print 'Min=%.3f Max=%.3f' % (min, max)

if band.GetOverviewCount() > 0:
    print 'Band has ', band.GetOverviewCount(), ' overviews.'

if not band.GetRasterColorTable() is None:
    print 'Band has a color table with ', \
                            band.GetRasterColorTable().GetCount(), 'entries.'

#######Reading Raster Data#####################################################

fmt = get_fmt_string('float', band.XSize)

xoff = 0
yoff = 0
xlines = band.XSize  # lineas a leer de x
ylines = 1  # lineas a leer de y
xbuff = band.XSize  # buffer de lineas de x a guardar
ybuff = 1  # buffer de lineas de y a guardar
datatype = gdalconst.GDT_Float32  # tipo de los datos

binary_string = band.ReadRaster(xoff, yoff, xlines, ylines,
                                xbuff, ybuff, datatype)


tuple_of_floats = struct.unpack(fmt, binary_string)
