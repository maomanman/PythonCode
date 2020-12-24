"""
GDAL 是处理栅格数据
OGR  是处理矢量数据

我的任务：
1、创建栅格  （网格）
2、矢量转栅格 （ 轨迹图转换成栅格图，可以向将轨迹图进行处理，如作业区域进行颜色填充等）
3、栅格叠加分析

2‘、是否可以直接栅格叠加矢量分析？

"""

# from osgeo import gdal, ogr
#
#
# '''
#     输出数据源中的图层
#     参数：fn 数据源的路径
#          is_write 打开数据源的模式，0 表示只读模式，1 表示读写模式
# '''
#
#
# def print_layers(fn, is_write):
#     ds = ogr.Open(fn, is_write)
#     if ds is None:
#         # raise OSError('Could not open %s', fn)
#         raise OSError('Could not open {}'.format(fn))
#     for i in range(ds.GetLayerCount()):
#         lyr = ds.GetLayer(i)
#         print('{0}:{1}'.format(i, lyr.GetName()))
#
# shp_fn = r'D:\mmm\python\轨迹测试数据\1112-gdal'
# print_layers(shp_fn,0)

######################### 无情的分割线
# import sys
# from osgeo import ogr
# import ospybook as pb
#
# fn = r'D:\mmm\python\轨迹测试数据\1112-gdal\2004-0019-GDAL.geojson'
# ds = ogr.Open(fn, 0)
# if ds is None:
#     sys.exit('Could not open {0}.'.format(fn))
#
# '''索引获取数据源中的图层方式'''
# lyr = ds.GetLayer(0)
# print(lyr.GetName())
#
# i = 0
# for fea in lyr:
#     pt = fea.geometry()
#     x = pt.GetX()
#     y = pt.GetY()
#     '''字段名称 获取属性值'''
#     code = fea.GetField('GBCODE')
#     '''对象方式获取属性值'''
#     length = fea.LENGTH
#     '''对象方式获取属性值2'''
#     lpoly_ = fea['LPOLY_']
#     '''索引方式获取属性值'''
#     fnode_ = fea.GetField(0)
#     '''获取特定类型的属性值'''
#     str_len = fea.GetFieldAsString('LENGTH')
#     print(code, length, fnode_, lpoly_, str_len, x, y)
#     i += 1
#     if i == 20:
#         break
#
# '''名称获取数据源中的图层'''
# lyr2 = ds.GetLayer('国家')
# print(lyr2.GetName())


######################## 无情的分割线

# from gdalconst import *
# from osgeo import gdal ,ogr
# import osr
# import sys
# import copy
#
# #叠加两个栅格图像（一个道路栅格图，一个土地利用类型图），两幅图像重叠的像元值都是第一个图像的值，
# #未重叠的像元值还是土地利用类型图上的值，最终结果便是土地利用类型图上面多了道路信息。
#
# roadFile =  r'D:\mmm\python\轨迹测试数据\1112-gdal\wallhaven-2em38y.jpg'
# landuseFile =  r'D:\mmm\python\轨迹测试数据\1112-gdal\wallhaven-967zyk.jpg'
# roadDs = gdal.Open(roadFile, GA_ReadOnly)
# landuseDs = gdal.Open(landuseFile, GA_ReadOnly)
# if roadDs is None:
#     print('Can not open {}'.format(roadFile))
#     sys.exit(1)
#
# geotransform = roadDs.GetGeoTransform()
# projection=roadDs.GetProjection()
# cols = roadDs.RasterXSize
# rows = roadDs.RasterYSize
# roadBand = roadDs.GetRasterBand(1)
# roadData = roadBand.ReadAsArray(0,0,cols,rows)
# # roadNoData = roadBand.GetNoDataValue()
# roadNoData= 0
#
# landuseBand = landuseDs.GetRasterBand(1)
# landuseData = landuseBand.ReadAsArray(0,0,cols,rows)
# # landuseNoData = landuseBand.GetNoDataValue()
# landuseNoData = 0
#
# result = landuseData
#
# for i in range(0,rows):
#     for j in range(0,cols):
#         if(abs(roadData[i,j] - 20) < 0.0001):
#            result[i,j] = 20
#         if((abs(landuseData[i,j] - landuseNoData)>0.0001) and (abs(roadData[i,j] - roadNoData) < 0.0001)):
#             result[i,j] = landuseData[i,j]
#         if((abs(landuseData[i,j] - landuseNoData)<0.0001) and (abs(roadData[i,j] - roadNoData) < 0.0001)):
#             result[i,j] = landuseNoData
# #write result to disk
# resultPath = r'D:\mmm\python\轨迹测试数据\1112-gdal\result_landuse.tif'
#
# format = "GTiff"
# driver = gdal.GetDriverByName(format)
# ds = driver.Create(resultPath, cols, rows, 1, GDT_Float32)
# ds.SetGeoTransform(geotransform)
# ds.SetProjection(projection)
# ds.GetRasterBand(1).SetNoDataValue(landuseNoData)
# ds.GetRasterBand(1).WriteArray(result)
# ds = None
#
# print('ok---------')

from osgeo import gdal, ogr
from gdalconst import *  # GDT_Byte
import sys

# 注册栅格数据驱动
# driver = gdal.GetDriverByName('TIFF')
# driver.Register()
filename = r'D:\mmm\python\轨迹测试数据\1112-gdal\qgis_raster.tif'
# cols = 1024
# rows = 1024
# outDataset = driver.Create(filename, cols, rows, 1, GDT_Byte)

roadDs = gdal.Open(filename, GA_ReadOnly)
if roadDs is None:
    print('Can not open {}'.format(filename))
    sys.exit(1)


geotransform = roadDs.GetGeoTransform()
projection=roadDs.GetProjection()
cols = roadDs.RasterXSize
rows = roadDs.RasterYSize
roadBand = roadDs.GetRasterBand(1)
roadData = roadBand.ReadAsArray(0,0,cols,rows)
roadNoData = roadBand.GetNoDataValue()
