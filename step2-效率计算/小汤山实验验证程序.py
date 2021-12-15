import pandas as pda


import alpha_shape.AlphaShapeForEdge as selfShape
from  alpha_shape.ZuoBiaoZhuanHuan import duFenMiao2du # 用于 度分秒 转 度


# 计算小汤山实验数据(经纬度坐标)的面积
def xiaoTangShanTest(sourceDataFile):
    """
    计算小汤山实验数据(经纬度坐标)的面积
    :return:
    """
    tangData = selfShape.GetData(sourceDataFile) # 将经纬度 坐标 转换成高斯坐标
    edge_x=tangData.x
    edge_y=tangData.y

    # 计算面积
    area, times = selfShape.calFiledArea([edge_x, edge_y])
    print("面积= {} 平方米".format(area))

# 计算小汤山实验数据（大地坐标）的面积
def xiaoTangShanTest2(sourceDataFile):
    """
    计算小汤山实验数据（大地坐标）的面积
    :return:
    """
    rootpath = r"D:\mmm\实验数据\0622-小汤山数据采集"
    tangData = pda.read_csv(rootpath + '/' + sourceDataFile)
    edge_x=tangData.E
    edge_y=tangData.N

    # 计算面积
    area, times = selfShape.calFiledArea([edge_x, edge_y])
    print("面积= {} 平方米".format(area))

# 根据边界点集 计算 面积
def calAreaByEdge(sourceDataFile):
    """
    根据边界点集 计算 面积
    :param sourceDataFile: 带全路径的边界点文件名
    :return:
    """
    # rootpath = r"D:\mmm\实验数据\test15\edgePoint"
    edgeData  = pda.read_excel( sourceDataFile)
    edge_x = edgeData.x
    edge_y = edgeData.y
    # 计算面积
    area, times = selfShape.calFiledArea([edge_x, edge_y])
    print("面积= {} 平方米".format(area))


########################################################################################

# data = duFenMiao2du(r'D:\mmm\实验数据\0622-小汤山数据采集\20210622_094800_bl_度分秒.csv')



# 1号边界-20210622_094800_小地块轨迹点.csv
# 2号边界-20210622_102702_中等地块轨迹点.csv
# 3号边界-20210622_132334-大地块轨迹点.csv
# xiaoTangShanTest(r"D:\mmm\实验数据\0623-分析小汤山采集数据\3号边界-20210622_132334-大地块轨迹点.csv")


# 4号边界-00146_edgePoint_R=7.98
# 5号边界-00719_edgePoint_R=12.1
# 6号边界-00514_edgePoint_R=10.51
calAreaByEdge(r"D:\mmm\实验数据\test15-坐标转换纠正\edgePoint\00514_edgePoint_R=10.51.xlsx")


