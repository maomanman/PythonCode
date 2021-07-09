import math
from pyproj import CRS
from pyproj import Transformer
from pyproj import _datadir, datadir  # 加上这个linux打包执行不报错
import pandas as pda
import numpy as npy


crs_WGS84 = CRS.from_epsg(4326)  # WGS84地理坐标系
crs_WebMercator = CRS.from_epsg(3857)  # Web墨卡托投影坐标系
cell_size = 0.009330691929342804  # 分辨率（米），一个像素表示的大小(24级瓦片)
origin_level = 24  # 原始瓦片级别
EarthRadius = 6378137.0  # 地球半径
tile_size = 256  # 瓦片大小


def GK2WGS84(x_y, d):
    """
    高斯坐标转WGS84坐标
    :param x_y: 高斯坐标x,y集合
    :param d: 带号
    :return: 纬度,经度集合
    """
    format = '+proj=tmerc +lat_0=0 +lon_0=' + str(d * 3) + ' +k=1 +x_0=500000 +y_0=0 +ellps=WGS84 +units=m +no_defs'
    crs_GK = CRS.from_proj4(format)
    transformer = Transformer.from_crs(crs_GK, crs_WGS84)
    lat_lon = transformer.itransform(x_y)
    return lat_lon


def WGS84ToWebMercator(lat_lon):
    """
    WGS84坐标转web墨卡托坐标
    :param lat_lon:  纬度,经度集合
    :return:  web墨卡托坐标x,y集合
    """
    transformer = Transformer.from_crs(crs_WGS84, crs_WebMercator)
    x_y = transformer.itransform(lat_lon)
    return x_y


def WebMercator2WGS84(x_y):
    """
    web墨卡托坐标转WGS84坐标
    :param x_y:  web墨卡托坐标x,y集合
    :return:  纬度,经度集合
    """
    transformer = Transformer.from_crs(crs_WebMercator, crs_WGS84)
    lat_lon = transformer.itransform(x_y)
    return lat_lon


def GK2WGS84_Single(x, y, d):
    """
    高斯坐标转WGS84坐标
    :param x: 高斯坐标x
    :param y: 高斯坐标y
    :param d: 带号
    :return: 纬度,经度
    """
    format = '+proj=tmerc +lat_0=0 +lon_0=' + str(d * 3) + ' +k=1 +x_0=500000 +y_0=0 +ellps=WGS84 +units=m +no_defs'
    crs_GK = CRS.from_proj4(format)
    transformer = Transformer.from_crs(crs_GK, crs_WGS84)
    lat, lon = transformer.transform(x, y)
    return lat, lon


def WGS84ToGK_Single(lat, lon):
    """
    WGS84坐标转高斯坐标
    :param lat:  WGS84坐标纬度
    :param lon:  WGS84坐标经度
    :return: 高斯坐标x,y
    """
    d = int((lon + 1.5) / 3)
    format = '+proj=tmerc +lat_0=0 +lon_0=' + str(d * 3) + ' +k=1 +x_0=500000 +y_0=0 +ellps=WGS84 +units=m +no_defs'
    crs_GK = CRS.from_proj4(format)
    transformer = Transformer.from_crs(crs_WGS84, crs_GK)
    x, y = transformer.transform(lat, lon)
    return x, y


def WGS84ToWebMercator_Single(lat, lon):
    """
    WGS84坐标转web墨卡托坐标
    :param lat:  WGS84坐标纬度
    :param lon:  WGS84坐标经度
    :return:  web墨卡托坐标x,y
    """
    transformer = Transformer.from_crs(crs_WGS84, crs_WebMercator)
    x, y = transformer.transform(lat, lon)
    return x, y


def WebMercator2WGS84_Single(x, y):
    """
    web墨卡托坐标转WGS84坐标
    :param x:  web墨卡托坐标x
    :param y:  web墨卡托坐标y
    :return:  纬度,经度
    """
    transformer = Transformer.from_crs(crs_WebMercator, crs_WGS84)
    lat, lon = transformer.transform(x, y)
    return lat, lon


def pixel2WebMercator(pixel, min_x, min_y, height, cell_size):
    """
    像素坐标转web墨卡托坐标
    :param pixel: 像素坐标
    :param min_x: web墨卡托坐标的最小x值
    :param min_y: web墨卡托坐标的最小y值
    :param height: 图片高
    :param cell_size: 地面分辨率（1像素代表多少米）
    :return: web墨卡托坐标
    """
    x = pixel[0] * cell_size + min_x
    y = (height - pixel[1]) * cell_size + min_y
    return x, y


def GK2WebMercator_Single(x, y, d):
    """
    高斯坐标转Web墨卡托坐标
    :param x: 高斯坐标x值
    :param y: 高斯坐标y值
    :param d: 带号
    :return: web墨卡托坐标
    """
    format = '+proj=tmerc +lat_0=0 +lon_0=' + str(d * 3) + ' +k=1 +x_0=500000 +y_0=0 +ellps=WGS84 +units=m +no_defs'
    crs_GK = CRS.from_proj4(format)
    transformer = Transformer.from_crs(crs_GK, crs_WebMercator)
    web_x, web_y = transformer.transform(x, y)
    return web_x, web_y


def web2Pixel(x, y, level):
    """
    Web墨卡托坐标转像素坐标
    :param x: Web墨卡托坐标x值
    :param y: Web墨卡托坐标y值
    :param level: 瓦片级别
    :return: 像素坐标
    """
    real_cell_size = cell_size * math.pow(2, (origin_level - level))
    pixel_x = math.floor((x + math.pi * EarthRadius) / real_cell_size)
    pixel_y = math.floor((math.pi * EarthRadius - y) / real_cell_size)
    return pixel_x, pixel_y


def pixel2Web(pixel_x, pixel_y, level):
    """
    像素坐标转Web墨卡托坐标
    :param pixel_x: 像素x坐标
    :param pixel_y: 像素y坐标
    :param level: 瓦片级别
    :return: web墨卡托坐标
    """
    real_cell_size = cell_size * math.pow(2, (origin_level - level))
    web_x = pixel_x * real_cell_size - (math.pi * EarthRadius)
    web_y = math.pi * EarthRadius - (pixel_y * real_cell_size)
    return web_x, web_y


def pixelGetTile(pixel):
    """
    计算像素所在的瓦片号
    :param pixel: 像素坐标
    :return: 瓦片行列号
    """
    tile_x = int(pixel[0] / tile_size)
    tile_y = int(pixel[1] / tile_size)
    return tile_x, tile_y


# 经纬度坐标 转 高斯坐标
def LatLon2GSXY(latitude, longitude):
    a = 6378137.0
    # b = 6356752.3142
    # c = 6399593.6258
    # alpha = 1 / 298.257223563
    e2 = 0.0066943799013
    # epep = 0.00673949674227


    #将经纬度转换为弧度
    latitude2Rad = (npy.pi / 180.0) * latitude

    beltNo = npy.int64((longitude + 1.5) / 3.0) #计算3度带投影度带号
    L = beltNo * 3 #计算3度带中央子午线经度

    # 判断是否存在 同时跨 两个3度带投影带的情况， 如果存在则 换成 6度带计算
    if beltNo[0]+1 in beltNo or beltNo[0]-1 in beltNo:
        beltNo = npy.int64((longitude + 3) / 6)  # 计算6度带投影度带号
        L = beltNo * 6 #计算6度带中央子午线经度

    l0 = longitude - L #经差
    tsin = npy.sin(latitude2Rad)
    tcos = npy.cos(latitude2Rad)
    t = npy.tan(latitude2Rad)
    m = (npy.pi / 180.0) * l0 * tcos
    et2 = e2 * npy.power(tcos, 2)
    et3 = e2 * npy.power(tsin, 2)
    X = 111132.9558 * latitude - 16038.6496 * npy.sin(2 * latitude2Rad) + 16.8607 * npy.sin(
        4 * latitude2Rad) - 0.0220 * npy.sin(6 * latitude2Rad)
    N = a / npy.sqrt(1 - et3)

    x = X + N * t * (0.5 * npy.power(m, 2) + (5.0 - npy.power(t, 2) + 9.0 * et2 + 4 * npy.power(et2, 2)) * npy.power(m, 4) / 24.0 + (
    61.0 - 58.0 * npy.power(t, 2) + npy.power(t, 4)) * npy.power(m, 6) / 720.0)
    y = 500000 + N * (m + (1.0 - npy.power(t, 2) + et2) * npy.power(m, 3) / 6.0 + (
    5.0 - 18.0 * npy.power(t, 2) + npy.power(t, 4) + 14.0 * et2 - 58.0 * et2 * npy.power(t, 2)) * npy.power(m, 5) / 120.0)

    return x, y




def XY2LatLon(X, Y, L0):

    iPI = 0.0174532925199433
    a = 6378137.0
    f= 0.00335281006247
    ZoneWide = 3 #按3度带进行投影

    ProjNo = int(X / 1000000)
    L0 = L0 * iPI
    X0 = ProjNo * 1000000 + 500000
    Y0 = 0
    xval = X - X0
    yval = Y - Y0

    e2 = 2 * f - f * f #第一偏心率平方
    e1 = (1.0 - math.sqrt(1 - e2)) / (1.0 + math.sqrt(1 - e2))
    ee = e2 / (1 - e2) #第二偏心率平方

    M = yval
    u = M / (a * (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256))

    fai = u \
          + (3 * e1 / 2 - 27 * e1 * e1 * e1 / 32) * math.sin(2 * u) \
          + (21 * e1 * e1 / 16 - 55 * e1 * e1 * e1 * e1 / 32) * math.sin(4 * u) \
          + (151 * e1 * e1 * e1 / 96) * math.sin(6 * u)\
          + (1097 * e1 * e1 * e1 * e1 / 512) * math.sin(8 * u)
    C = ee * math.cos(fai) * math.cos(fai)
    T = math.tan(fai) * math.tan(fai)
    NN = a / math.sqrt(1.0 - e2 * math.sin(fai) * math.sin(fai))
    R = a * (1 - e2) / math.sqrt(
        (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)))
    D = xval / NN

    #计算经纬度（弧度单位的经纬度）
    longitude1 = L0 + (D - (1 + 2 * T + C) * D * D * D / 6 + (
    5 - 2 * C + 28 * T - 3 * C * C + 8 * ee + 24 * T * T) * D * D * D * D * D / 120) / math.cos(fai)
    latitude1 = fai - (NN * math.tan(fai) / R) * (
    D * D / 2 - (5 + 3 * T + 10 * C - 4 * C * C - 9 * ee) * D * D * D * D / 24 + (
    61 + 90 * T + 298 * C + 45 * T * T - 256 * ee - 3 * C * C) * D * D * D * D * D * D / 720)

    #换换为deg
    longitude = longitude1 / iPI
    latitude = latitude1 / iPI

    return latitude, longitude


def duFenMiao2du(sourceFile):
    """
    将经纬度 度分秒 转换成 度；文件中的经纬度是由度分秒表示，且都是由符号表示，如：40°11'00.20525"
    :param sourceFile: 带全路径的文件名源
    :return: 返回原文件，并加入转换成度后的 经纬度
    """

    data = pda.read_csv(sourceFile)
    for i in data.index:
        lat = int(data.loc[i,'纬度'].split('°')[0]) + int(data.loc[i,'纬度'].split('°')[1].split('\'')[0])/60+float(data.loc[i,'纬度'].split('°')[1].split('\'')[1].split('\"')[0])/3600
        data.loc[i, '纬度2'] = lat
        lot = int(data.loc[i,'经度'].split('°')[0]) + int(data.loc[i,'经度'].split('°')[1].split('\'')[0])/60+float(data.loc[i,'经度'].split('°')[1].split('\'')[1].split('\"')[0])/3600
        data.loc[i, '经度2'] = lot

    return data


#
# print LatLon2GSXY(40.07837722329, 116.23514827596)
# print XY2LatLon(434760.7611718801, 4438512.040474475, 117.0)

if __name__ == '__main__':
    data = pda.read_csv(r'D:\mmm\python\轨迹测试数据\1112-gdal\皖11-2004_2016-10-04==1004-0019-field.csv')

    # x ,y = WGS84ToGK_Single(data.loc[:,'纬度'], data.loc[:,'经度'])

    # x1, y1 = WGS84ToGK_Single(27.13617383, 109.7349437)



