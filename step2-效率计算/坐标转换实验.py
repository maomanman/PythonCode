import math
import numpy as npy
import pandas  as pda


# 经纬度转墨卡托
def lonlat2mercattor(lonlat):
    mercator = {'x': 0, 'y': 0}
    x = lonlat['x'] * 20037508.34 / 180
    y = math.log(math.tan((90 + lonlat['y']) * math.pi / 360)) / (math.pi / 180)
    y = y * 20037508.34 / 180
    mercator['x'] = x
    mercator['y'] = y
    return mercator


def LatLon2GSXY(latitude, longitude):
    a = 6378137.0
    # b = 6356752.3142
    # c = 6399593.6258
    # alpha = 1 / 298.257223563
    e2 = 0.0066943799013
    # epep = 0.00673949674227

    # 将经纬度转换为弧度
    latitude2Rad = (npy.pi / 180.0) * latitude

    beltNo = npy.int8((longitude + 1.5) / 3.0)  # 计算3度带投影度带号
    L = beltNo * 3  # 计算3度带中央子午线经度
    l0 = longitude - L  # 经差
    tsin = npy.sin(latitude2Rad)
    tcos = npy.cos(latitude2Rad)
    t = npy.tan(latitude2Rad)
    m = (npy.pi / 180.0) * l0 * tcos
    et2 = e2 * npy.power(tcos, 2)
    et3 = e2 * npy.power(tsin, 2)
    X = 111132.9558 * latitude - 16038.6496 * npy.sin(2 * latitude2Rad) + 16.8607 * npy.sin(
        4 * latitude2Rad) - 0.0220 * npy.sin(6 * latitude2Rad)
    N = a / npy.sqrt(1 - et3)

    x = X + N * t * (0.5 * npy.power(m, 2) + (5.0 - npy.power(t, 2) + 9.0 * et2 + 4 * npy.power(et2, 2)) * npy.power(m,
                                                                                                                     4) / 24.0 + (
                             61.0 - 58.0 * npy.power(t, 2) + npy.power(t, 4)) * npy.power(m, 6) / 720.0)
    y = 500000 + N * (m + (1.0 - npy.power(t, 2) + et2) * npy.power(m, 3) / 6.0 + (
            5.0 - 18.0 * npy.power(t, 2) + npy.power(t, 4) + 14.0 * et2 - 58.0 * et2 * npy.power(t, 2)) * npy.power(m,
                                                                                                                    5) / 120.0)

    return x, y


def LatLon2XY2(latitude, longitude):
    a = 6378137.0
    # b = 6356752.3142
    # c = 6399593.6258
    # alpha = 1 / 298.257223563
    e2 = 0.0066943799013
    # epep = 0.00673949674227


    #将经纬度转换为弧度
    latitude2Rad = (math.pi / 180.0) * latitude

    beltNo = int((longitude + 1.5) / 3.0) #计算3度带投影度带号
    L = beltNo * 3 #计算中央经线
    l0 = longitude - L #经差
    tsin = math.sin(latitude2Rad)
    tcos = math.cos(latitude2Rad)
    t = math.tan(latitude2Rad)
    m = (math.pi / 180.0) * l0 * tcos
    et2 = e2 * pow(tcos, 2)
    et3 = e2 * pow(tsin, 2)
    X = 111132.9558 * latitude - 16038.6496 * math.sin(2 * latitude2Rad) + 16.8607 * math.sin(
        4 * latitude2Rad) - 0.0220 * math.sin(6 * latitude2Rad)
    N = a / math.sqrt(1 - et3)

    x = X + N * t * (0.5 * pow(m, 2) + (5.0 - pow(t, 2) + 9.0 * et2 + 4 * pow(et2, 2)) * pow(m, 4) / 24.0 + (
    61.0 - 58.0 * pow(t, 2) + pow(t, 4)) * pow(m, 6) / 720.0)
    y = 500000 + N * (m + (1.0 - pow(t, 2) + et2) * pow(m, 3) / 6.0 + (
    5.0 - 18.0 * pow(t, 2) + pow(t, 4) + 14.0 * et2 - 58.0 * et2 * pow(t, 2)) * pow(m, 5) / 120.0)

    return x, y

def wgs2gs(latitude, longitude):
    """
    wgs84 转 高斯
    参考文献：2015-基于拖拉机作业轨迹的农田面积测量_鲁植雄.pdf
    :param latitude:
    :param longitude:
    :return:
    """
    a = 6378137  # 单位 米，地球长半轴
    b = 6356752.3  # 单位 米，地球短半轴
    e2 = math.sqrt((math.pow(a, 2) - math.pow(b, 2)) / math.pow(b, 2))  # 第二偏心率

    b1 = 1 - (3 / 4) * math.pow(e2, 2) + (45 / 65) * math.pow(e2, 4) - (175 / 256) * math.pow(e2, 6) + (
                11025 / 16384) * math.pow(e2, 8)
    b2 = b1 - 1
    b4 = (12 / 32) * math.pow(e2, 4) - (175 / 384) * math.pow(e2, 6) - (3675 / 8192) * math.pow(e2, 8)
    b6 = -(35 / 96) * math.pow(e2, 6) + (735 / 2048) * math.pow(e2, 8)
    b8 = (315 / 1024) * math.pow(e2, 8)


def duFenMiao2du():
    """ 将经纬度 度分秒 转换成 度"""
    data = pda.read_csv(r"D:\mmm\实验数据\0623-分析小汤山采集数据\20210622_102702_bl.csv")
    for i in data.index:
        lat = int(data.loc[i,'纬度'].split('°')[0]) + int(data.loc[i,'纬度'].split('°')[1].split('\'')[0])/60+float(data.loc[i,'纬度'].split('°')[1].split('\'')[1].split('\"')[0])/3600
        data.loc[i, '纬度2'] = lat
        lot = int(data.loc[i,'经度'].split('°')[0]) + int(data.loc[i,'经度'].split('°')[1].split('\'')[0])/60+float(data.loc[i,'经度'].split('°')[1].split('\'')[1].split('\"')[0])/3600
        data.loc[i, '经度2'] = lot

    data.to_csv(r"D:\mmm\实验数据\0623-分析小汤山采集数据\20210622_102702_bl.csv")


# # lonlat = {'x': 117.5972195, 'y': 37.81087267}
# # m = lonlat2mercattor(lonlat)
# m1=LatLon2GSXY(40.180373341661,116.44299478933)
# print(m1)
# m2=LatLon2XY2(40.180373341661,116.44299478933)
#
# print(m2)

duFenMiao2du()