import  os
"""
本文件用于存放一些公共变量
"""

class globalVal:
    debug = 0  # 1-表调试打印 0- 不打印

    mapName = 'san_map.html' #卫星底图 + 轨迹路劲
    workMapName = 'poin_map.html'  # 卫星底图 + 轨迹点
    edgeMapName = 'edge_map.html' # 卫星底图 + 边界线

    imageBasePath = r'D:\mmm\轨迹数据集\轨迹图汇总\edgeImage'
    fileBasePath = r'D:\mmm\轨迹数据集\汇总'
    edgeBasePath = r'D:\mmm\轨迹数据集\轨迹图汇总\edgePoint'

    # 加载外部的web界面
    path = 'file://\\' + os.getcwd() + '\\' + mapName
    mapPath = path.replace("\\", "/")

    path = 'file://\\' + os.getcwd() + '\\' + workMapName
    workMapPath= path.replace("\\", "/")

    path = 'file://\\' + os.getcwd() + '\\' + edgeMapName
    edgeMapPath = path.replace("\\", "/")

