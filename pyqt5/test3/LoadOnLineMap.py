import numpy as np
import folium # 用于显示地图
from folium import plugins
import psycopg2 # 用于链接postgre数据库
import sys
import os
import glob # 用于模糊匹配
import pandas as pd #用于读取excel文件
from globalVal import globalVal

import time

# global debug
# debug = 1 # 打印调试信息

# # 天地图遥感
# class TDT_img(cimgt.GoogleWTS):
#     def _image_url(self, tile):
#         x, y, z = tile
#         key = 'f6d6b62718ce1e3f102f2f50dfa9228b'
#         url = 'http://t0.tianditu.gov.cn/DataServer?T=img_w&x=%s&y=%s&l=%s&tk=%s' % (x, y, z, key)
#         return url

def fromFileIdGetLatLon(fileID = 1,fileType=1):
    """
    根据文件序号读取经纬度数据,
    :param fileType: 1-读取所有的点  2-读取边界点 3-区分工作点和非工作点
    :param fileID:
    :return:经度，纬度
    """

    if fileType == 2:
        #从文件中读取边界点
        fileName = glob.glob(os.path.join(globalVal.edgeBasePath, str(fileID).zfill(5)) + '_edgePoint_R*')
    else: #fileType == 1  ==3
        # 从文件中读取轨迹点
        fileName = glob.glob(os.path.join(globalVal.fileBasePath, str(fileID).zfill(5)) + ' *')


    data = pd.read_excel(fileName[0])
    col = data.columns #  col[3]='纬度'lat  col[2]='经度'log

    if fileType == 3:
        data.sort_values(by='工作状态', inplace=True, ascending=False) # 工作点排在前，非工作点排在后
        data.reset_index(drop=True, inplace=True) # 更新索引

        splitPoint = data[data['工作状态']==True].shape[0]
        data1 = data.loc[:splitPoint,:].copy()
        data2 = data.loc[splitPoint:,:]
        data1.loc[splitPoint]=[0]*len(col)
        data = pd.concat([data1,data2],ignore_index=True)
        # col = dat.columns

        pass
    return list(data[col[3]]),list(data[col[2]])




def PlotLineOnMap(fileID = 1,fileType=1):
    """
    加载线上地图，并根据文件序号显示对应轨迹点
    :param fileType: 1-读取所有的点  2-读取边界点 3-区分工作点和非工作点
    :param fileID:
    :return:
    """
    if globalVal.debug:
        print("文件序号",fileID)



    Lat,Lon = fromFileIdGetLatLon(fileID,fileType)

    # # 给出的坐标系为GCJ-02，如果需要测试google地图，需要进行坐标转换
    # Lat = [40.8352, 40.8342, 40.8335, 40.8323, 40.8311, 40.8308, 40.8304, 40.8315, 40.8325, 40.8332, 40.8339,
    #        40.8345,
    #        40.8352]
    # Lon = [114.8886, 114.8883, 114.8881, 114.8877, 114.8873, 114.8888, 114.8902, 114.8909, 114.8916, 114.8919,
    #        114.8922,
    #        114.8917, 114.8886]

    tri = np.array(list(zip(Lat, Lon)))

    if fileType==3:
        locationLat=np.sum(Lat)/(len(Lat)-1)
        locationLon = np.sum(Lon)/(len(Lon)-1)
        pass
    else:
        locationLat = np.mean(Lat)
        locationLon = np.mean(Lon)
    san_map = folium.Map(
        location=[locationLat, locationLon],
        zoom_start=16,#初始缩放比例
        # tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
        # 高德街道图
        # tiles='http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', # 高德卫星图
        # 天地图遥感底图
        tiles='https://t1.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=6c334c0cc38a2582f75d0dbff2d2a080',
        attr='default')

    # folium.PolyLine(tri, color='#3388ff',weight = 2).add_to(san_map)
    # marker_cluster = plugins.MarkerCluster().add_to(san_map)
    # for lat, lon in zip(Lat, Lon):
    #     folium.Marker([lat, lon], color='red').add_to(marker_cluster)

    if fileType == 1:
        folium.PolyLine(tri, color='#3388ff', weight=2).add_to(san_map)
        san_map.save(globalVal.mapName)

    elif fileType == 2:
        folium.PolyLine(tri, color='#3388ff', weight=2).add_to(san_map)
        san_map.save((globalVal.edgeMapName))

    elif fileType==3:
        pointColor ='red'

        # 工作点和非工作点区分显示
        # for lat, lon in zip(Lat, Lon):
        #     if lat==0 and lon==0:
        #         pointColor = 'beige'
        #         continue
        #     folium.Circle(
        #         radius=0.1,
        #         location=[lat, lon],
        #         color=pointColor,
        #         fill=True,
        #         fill_color=pointColor,
        #         fill_opacity=0.1,
        #     ).add_to(san_map)

        # 只显示非工作点
        splitPoint = Lat.index(0)+1

        for lat, lon in zip(Lat[splitPoint:], Lon[splitPoint:]):

            folium.Circle(
                radius=0.1,
                location=[lat, lon],
                color="beige",
                fill=True,
                fill_color=pointColor,
                fill_opacity=0.1,
            ).add_to(san_map)
        san_map.save((globalVal.workMapName))




if __name__ == "__main__":
    PlotLineOnMap(1,3)
    PlotLineOnMap(1, 1)
    # fromFileIdGetLatLon()
    # lat,lon = fromFileIdGetLatLon()

    # print(type(lat))