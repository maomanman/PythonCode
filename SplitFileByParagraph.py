import pandas as pda
import numpy as npy
import math as ma
import time
import datetime
import os
# 这两个是用于的打开文件选择框
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# 这些是用来读写excel文件的
import xlwt
import xlrd
from xlutils.copy import copy


def GetSectionFileName(sourFileName, GpsTime, tpyeFlag=1):
    """
    获取切片文件名
    根据原文件名，和 切片文件第一个GPS时间，以及类型标志（1=地块、0=道路，默认是地块）拼写切片文件名
    :param sourFileName:  原文件名称
    :param GpsTime: 切片文件第一个轨迹点的GPS时间
    :param tpyeFlag: 类型标志:1-地块，0-道路
    :return: 切片文件名
    """

    monthAndDay = "{:02d}{:02d}".format(GpsTime.month, GpsTime.day)
    hourAndMinute = "{:02d}{:02d}".format(GpsTime.hour, GpsTime.minute)

    sf = sourFileName.split('.')

    if tpyeFlag == 1:
        sectionFileName = sf[0] + '==' + monthAndDay + '-' + hourAndMinute + '-field.' + sf[1]
    else:
        sectionFileName = sf[0] + '==' + monthAndDay + '-' + hourAndMinute + '-road.' + sf[1]

    return sectionFileName

def RegisterForNewSectionFile(regFileName, values):
    """
    将切片的文件信息进行登记记录
    :param regFileName:  登记册文件名
    :param values: 需要登记的文件信息
    :return:
    """
    readFile = xlrd.open_workbook(regFileName, formatting_info=True)

    writeData = copy(readFile)
    writeSave = writeData.get_sheet(0)
    oldRowNum = readFile.sheet_by_index(0).nrows  # 获取表格中已存在的数据的行数
    for i in range(len(values)):
        writeSave.write(oldRowNum + i, 3, values[i][0])
        for j in range(1, len(values[i])):
            writeSave.write(oldRowNum + i, 7 + j, values[i][j])

    writeData.save(regFileName)


"""
使用方法介绍：
    给出要分割的  文件名(带地址的) fileName，然后分割的索引号分段文件paraName
    最后按照分段文件的分段分割文件，分割后的小文件单独写在一个文件夹中，文件夹用需要分割是文件名命名，如果文件夹存在则直接写小文件，文件夹不存在则创建文件夹
    
    将分割后的文件信息登记到 regFileName ，注意 道路轨迹 和 地块轨迹的 的标记是需要手工更改的
"""



fileName = "D:/mmm/python/轨迹测试数据/0930/皖11-2004_2016-10-04.xlsx"
data = pda.read_excel(fileName)
data.set_index('序列号',inplace=True)
columns_array = data.columns.array  # 列标签名

paraName="D:/mmm/python/轨迹测试数据/0930/绕行法地块分段.xlsx"
pData =pda.read_excel(paraName)

filePath = os.path.split(fileName)
splitPointPath = filePath[0] + '/' + filePath[1].split('.')[0] + '-section2'
if not os.path.exists(splitPointPath):
    os.mkdir(splitPointPath)
splitPointExeclName = splitPointPath + '/皖11-2004_2016-10-04.xlsx'

paraNo=pData.shape[0]
registerInfo = []

count = len(pData.loc[:,'2004起'].dropna(axis=0,how='all')) # 删除空行数据
value = ['道路']

for i in range(count):
    start = pData.loc[i,'2004起']
    end = pData.loc[i,'2004止']

    step = int(end-start+1)
    countOfWorkPoint =int(sum(data.loc[start:end,columns_array[2]]))
    sectionFileName = GetSectionFileName(splitPointExeclName, data.loc[start, 'GPS时间'],0) # 0-道路  1-地块
    countOfValidPoint= int(sum(data.loc[start:end,columns_array[1]] >= data.loc[start:end,columns_array[9]]))  # 作业深度 >= 标准深度

    samplingTime = data.loc[start:end, '时间间隔'].mode()[0].second # 时间间隔的 众数
    strTime = str(data.loc[end, 'GPS时间'] - data.loc[start, 'GPS时间']).split(' days ')
    strDay = strTime[1].split(':')
    strDay[0] = str(24 * int(strTime[0]) + int(strDay[0]))
    totalTime = ':'.join(strDay)
    sectionFileNameOfNOTpath = os.path.split(sectionFileName)[1]
    value.extend([step, countOfWorkPoint, countOfValidPoint, samplingTime, str(data.loc[start, 'GPS时间']),
                  str(data.loc[end, 'GPS时间']), totalTime, sectionFileNameOfNOTpath])
    registerInfo.append(value)
    data.loc[start:end].to_excel(sectionFileName)

regFileName = 'D:/mmm/python/轨迹测试数据/0930/轨迹索引-0930.xls'
RegisterForNewSectionFile(regFileName, registerInfo)