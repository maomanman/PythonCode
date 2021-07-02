import pandas as pda
import numpy as np
import math
import datetime
import time

import alpha_shape.AlphaShapeForEdge as selfShape
from alpha_shape.ZuoBiaoZhuanHuan import LatLon2GSXY
from alpha_shape.ZuoBiaoZhuanHuan import WGS84ToWebMercator


def paraWorkTime(paraData, yangT):
    """
    计算一段时间段内的有效工作时长：在计算总时长的基础上加上对工作属性的限定
    :param paraData: 一段时间内的轨迹点
    :param yangT: 采样时间
    :return: 这段时间内的有效工作时长
    """
    yangT = pda.to_timedelta(yangT,unit='s')
    paraData = paraData[paraData['工作状态'] == True]  # 筛选工作点
    paraData.reset_index(drop=True, inplace=True)
    count = paraData.shape[0]

    sumTime = pda.to_timedelta(0)
    startPoint = 0
    for ind in paraData.index:
        if ind == 0:
            continue

        # 判断序列号是否连续
        gapInd = paraData.loc[ind, '序列号'] - paraData.loc[ind - 1, '序列号']
        if gapInd > 1:  # 序列号不连续
            endPoint = ind - 1

            # 计算此段时间差
            t1 = paraData.loc[startPoint, 'GPS时间']
            t2 = paraData.loc[endPoint, 'GPS时间']
            if type(t2) == str:
                t1 = pda.Timestamp(t1)
                t2 = pda.Timestamp(t2)
            paraGapT = t2 - t1
            if paraGapT.total_seconds() == 0:  # 孤立的一个工作点,其工作时间记为采样时间
                paraGapT = yangT
            sumTime = sumTime + paraGapT

            startPoint = ind  # 下一个连续时间段的起始点

    if count > 0:
        endPoint = count - 1

        if endPoint == startPoint:
            paraGapT = yangT
        else:
            # 计算此段时间差
            t1 = paraData.loc[startPoint, 'GPS时间']
            t2 = paraData.loc[endPoint, 'GPS时间']
            if type(t2) == str:
                t1 = pda.Timestamp(t1)
                t2 = pda.Timestamp(t2)
            paraGapT = t2 - t1

        sumTime = sumTime + paraGapT



    return sumTime


def aFileWorkTime(fileName, yangT, paraTimeList):
    """
    获得一个地块轨迹文件的有效工作时间：根据工作状态判断
    :param fileName: 轨迹文件名
    :param yangT: 采样时间
    :param paraTimeList: 时间段起止序列号的列表
    :return: 有效工作时间
    """
    fileData = pda.read_excel('D:/mmm/轨迹数据集/汇总/' + fileName)

    paraNum = len(paraTimeList)  # 时间段个数
    sumWorkTime = pda.to_timedelta(0)

    for i in range(0, paraNum):
        # 获取 时间段 起止序列号
        startPoint = int(paraTimeList[i].split(', ')[0])
        endPoint = int(paraTimeList[i].split(', ')[1])

        # 获取时间段轨迹点数据
        paraData = fileData[fileData['序列号'] >= startPoint]
        paraData = paraData[paraData['序列号'] <= endPoint]

        paraTime = paraWorkTime(paraData,yangT)

        sumWorkTime = sumWorkTime  + paraTime
        # print(i)

    return sumWorkTime

def batchGetWorkTime():
    """
    批量获取所有地块作业时间
    :return:
    """

    rootPath = r'D:\mmm\实验数据\test22-统计有效工作时间'
    # 通过索引表获取 各个文件的 文件名、采样时间
    fileIndexData = pda.read_excel(rootPath + '/test22-轨迹索引-v1.0.xlsx')

    # 读取 test21  的 结果表，获取各个时间段的起止序列号列表
    test22_ParaTimeList = pda.read_excel(rootPath + '/test22_段落起止序列号.xlsx')

    test22_return_info = pda.DataFrame(columns=['文件名称','总工作时长','有效工作时长','总工作时长(s)','有效工作时长(s)'])

    for ind in fileIndexData.index:
        fileName = fileIndexData.loc[ind,'文件名称']
        if fileName == test22_ParaTimeList.loc[ind,'文件名称']:
            # print(fileName)
            # print(test22_ParaTimeList.loc[ind,'文件名称'])
            # print('\n')
            print(fileIndexData.loc[ind,'新文件序号'])
            yangT = fileIndexData.loc[ind,'采样时间']
            paraTimeL = test22_ParaTimeList.loc[ind,'各个时间段起止序列号'] # 是一个字符串

            paraTimeL = paraTimeL.split('), (')
            paraTimeL[0]=paraTimeL[0].replace('[(','')
            paraTimeL[len(paraTimeL)-1] = paraTimeL[len(paraTimeL)-1].replace(')]', '')

            workTime = aFileWorkTime(fileName,yangT,paraTimeL)
            totalTime = test22_ParaTimeList.loc[ind,'总工作时长']

            test22_return_info.loc[ind]=[fileName,totalTime,str(workTime),pda.to_timedelta(totalTime,unit='s').total_seconds(),workTime.total_seconds()]


        if ind % 10 ==0:
            test22_return_info.to_excel(rootPath + '/test22_return_info.xlsx')

    test22_return_info.to_excel(rootPath + '/test22_return_info.xlsx')



#
# data = pda.read_excel("D:/mmm/轨迹数据集/汇总/00051 耕-大-斜==黑10-467619_2020-11-2==1101-2343-filed.xlsx")
# #
# data = data[data['序列号'] >= 5936]
# data = data[data['序列号'] <= 5936]
# t = paraWorkTime(data, 4)
# print(t)

# [(5765, 7441), (8000, 8330), (8331, 9048), (9275, 9364), (9365, 11612), (13067, 15767)]
# [(198, 207), (208, 2160), (2161, 3130), (3131, 5935), (5936, 5936), (5937, 6326), (6870, 16596), (16597, 25099)]
paraTimeL='[(2631, 3523)]'
paraTimeL = paraTimeL.split('), (')
paraTimeL[0]=paraTimeL[0].replace('[(','')
paraTimeL[len(paraTimeL)-1] = paraTimeL[len(paraTimeL)-1].replace(')]', '')
t = aFileWorkTime("00195 耕-小-梭==鲁16-543101_2018-10-14==1014-0327-filed.xlsx",2,paraTimeL)
print(t)

#
# batchGetWorkTime()