import pandas as pda
import random
import time

import alpha_shape.AlphaShapeForEdge as selfShape
from alpha_shape.ZuoBiaoZhuanHuan import LatLon2GSXY


def fromSourceDataGetEdgeAndArea(sourceDataFile=''):
    """
    根据原始轨迹点 检测 边界点，获取边界图、获取边界坐标文件、计算地块面积

    ** 特别注意，这里需要手动设置 alpha shape 半径
    :param sourceDataFile: 原始轨迹点文件名（全路径文件名）
    :return:
    """
    # D:\mmm\轨迹数据集\汇总 D:\mmm\实验数据\test15\sinan
    rootpath = r"D:\mmm\轨迹数据集\汇总"

    # 此函数可将原始文件中的经纬度坐标转换成高斯坐标，便于后面边界检测和面积计算
    sData = selfShape.GetData(rootpath+ '/'+sourceDataFile)
    sData.to_excel(rootpath + '/sourceData.xlsx')

    # alpha shape 算法的半径，需要通过某种方式获取，目前还未进行总结
    # TODO   alpha shape 算法的半径，需要通过某种方式获取，目前还未进行总结
    radius =7.7
    #
    # 通过 alpha shape 算法 获取地块边界点
    edge_x, edge_y, edge_index = selfShape.alpha_shape_2D(sData, radius)
    #
    # # # 对边界点进行文档保存
    # edgeData = pda.DataFrame({'pointIndex': edge_index, 'x': edge_x, 'y': edge_y})
    # flag = time.strftime("%m%d%H%M%S", time.localtime())
    # # edgeData.to_csv(rootpath + '/edge_'+flag+'.csv')
    # #
    # # 对边界点的其他信息点信息进行保存
    # dd = sData[sData['工作状态'] == True]
    # dd.set_index('序列号',inplace=True)
    # dd.loc[edge_index].to_excel(rootpath + '/edgePointInfo_'+flag+'.xlsx')
    #
    #
    # # # 绘制边界图并进行保存
    # selfShape.plotEdgefor12(sData,edge_x,edge_y,rootpath+'/image_'+flag+'.jpg')

    # 计算面积
    area, times = selfShape.calFiledArea([edge_x, edge_y])
    print("面积= {} 平方米".format(area))

def xiaoTangShanTest(sourceDataFile):
    """
    计算小汤山实验数据(经纬度坐标)的面积
    :return:
    """
    rootpath = r"D:\mmm\实验数据\0623-分析小汤山采集数据"
    tangData = selfShape.GetData(rootpath+ '/'+sourceDataFile)
    edge_x=tangData.x#.x#.E
    edge_y=tangData.y#y#.N

    # 计算面积
    area, times = selfShape.calFiledArea([edge_x, edge_y])
    print("面积= {} 平方米".format(area))


def xiaoTangShanTest2(sourceDataFile):
    """
    计算小汤山实验数据（大地坐标）的面积
    :return:
    """
    rootpath = r"D:\mmm\实验数据\0622-小汤山数据采集"
    tangData = pda.read_csv(rootpath + '/' + sourceDataFile)
    edge_x=tangData.E#.x#.E
    edge_y=tangData.N#y#.N

    # 计算面积
    area, times = selfShape.calFiledArea([edge_x, edge_y])
    print("面积= {} 平方米".format(area))

def calAreaByEdge(sourceDataFile):
    rootpath = r"D:\mmm\实验数据\test15\edgePoint"
    edgeData  = pda.read_excel(rootpath + '/' + sourceDataFile)
    edge_x = edgeData.x  # .x#.E
    edge_y = edgeData.y  # y#.N

    # 计算面积
    area, times = selfShape.calFiledArea([edge_x, edge_y])
    print("面积= {} 平方米".format(area))


# 00231 耕-大-梭==鲁17-530111_2019-10-14==1014-0354-filed.xlsx
# 00435 耕-大-梭==新31-998227_2020-3-26==0326-0201-filed.xlsx
# fromSourceDataGetEdgeAndArea('00685 种-大-梭==辽12-40212_2020-04-30==0430-1410-filed.xlsx ')

# 20210622_094800_小地块轨迹点.csv
# 20210622_102702_中等地块轨迹点.csv
# 20210622_132334-大地块轨迹点.csv
# 1号边界-20210622_094800_小地块轨迹点.csv
# 2号边界-20210622_102702_中等地块轨迹点.csv
# 3号边界-20210622_132334-大地块轨迹点.csv

# 3号边界-20210622_132334-大地块轨迹点-转换.csv
# 20210622_132334-bl_change.csv

# xiaoTangShanTest("")
# xiaoTangShanTest2("20210622_102702_中等地块轨迹点.csv")

# 4号边界-00146_edgePoint_R=7.98.csv
# 5号边界-00719_edgePoint_R=12.1
# 6号边界-00514_edgePoint_R=10.51

calAreaByEdge("00514_edgePoint_R=10.51.xlsx")


