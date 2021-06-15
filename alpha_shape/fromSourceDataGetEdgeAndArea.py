import pandas as pda
import random
import time

import alpha_shape.AlphaShapeForEdge as selfShape
from alpha_shape.ZuoBiaoZhuanHuan import LatLon2GSXY


def fromSourceDataGetEdgeAndArea(sourceDataFile):
    """
    根据原始轨迹点 检测 边界点，获取边界图、获取边界坐标文件、计算地块面积
    :param sourceDataFile: 原始轨迹点文件名（全路径文件名）
    :return:
    """

    rootpath = r"D:\mmm\实验数据\0615"

    # 此函数可将原始文件中的经纬度坐标转换成高斯坐标，便于后面边界检测和面积计算
    sData = selfShape.GetData(rootpath+ '/'+sourceDataFile)
    sData.to_excel(rootpath + '/data.xlsx')

    # alpha shape 算法的半径，需要通过某种方式获取，目前还未进行总结
    # TODO   alpha shape 算法的半径，需要通过某种方式获取，目前还未进行总结
    radius = 5.8

    # 通过 alpha shape 算法 获取地块边界点
    edge_x, edge_y, edge_index = selfShape.alpha_shape_2D(sData, radius)

    # 对边界点进行文档保存
    edgeData = pda.DataFrame({'pointIndex': edge_index, 'x': edge_x, 'y': edge_y})
    flag = time.strftime("%m%d%H%M%S", time.localtime())
    edgeData.to_csv(rootpath + '/edge_'+flag+'.csv')

    # 对边界点的其他信息点信息进行保存
    dd = sData[sData['工作状态'] == True]
    dd.set_index('序列号',inplace=True)
    dd.loc[edge_index].to_excel(rootpath + '/edgePointInfo_'+flag+'.xlsx')

    # 绘制边界图并进行保存
    selfShape.plotEdgefor12(sData,edge_x,edge_y,rootpath+'/image_'+flag+'.jpg')

    # 计算面积
    area, times = selfShape.calFiledArea([edge_x, edge_y])
    print("面积= {} 平方米".format(area))

fromSourceDataGetEdgeAndArea("00189 耕-小-绕==鲁16-543101_2018-11-3==1103-0859-filed.xlsx")





