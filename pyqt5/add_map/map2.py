import numpy as np
import folium
from folium import plugins


def PlotLineOnMap():
    # 给出的坐标系为GCJ-02，如果需要测试google地图，需要进行坐标转换
    Lat = [40.8352, 40.8342, 40.8335, 40.8323, 40.8311, 40.8308, 40.8304, 40.8315, 40.8325, 40.8332, 40.8339, 40.8345,
           40.8352]
    Lon = [114.8886, 114.8883, 114.8881, 114.8877, 114.8873, 114.8888, 114.8902, 114.8909, 114.8916, 114.8919, 114.8922,
           114.8917, 114.8886]
    tri = np.array(list(zip(Lat, Lon)))

    san_map = folium.Map(
        location=[40.8329, 114.8898],
        zoom_start=16,
        tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',  # 高德街道图
        # tiles='http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', # 高德卫星图
        attr='default')

    folium.PolyLine(tri, color='#3388ff').add_to(san_map)
    marker_cluster = plugins.MarkerCluster().add_to(san_map)
    for lat, lon in zip(Lat, Lon):
        folium.Marker([lat, lon], color='red').add_to(marker_cluster)
    san_map.save('test.html')


def main():
    PlotLineOnMap()


if __name__ == '__main__':
    main()