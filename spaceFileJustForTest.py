import pandas as pda
import numpy as np
import math
import matplotlib.pyplot as plt
import xlwt
import xlrd
from xlutils.copy import copy

import tkinter.messagebox
from tkinter.filedialog import *

# dff = pda.dataframe(np.random.randint(20,size=(10,5)),columns=list('abcde'))

"""
求众数
data['时间间隔'].mode()
"""


def mode():
    data = pda.read_excel('D:/mmm/python/轨迹测试数据/0927-将文件进行分割成多个文件/轨迹索引.xlsx')
    print(data.shape[0])
    del data


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
    oldRowNum = writeSave.nrows  # 获取表格中已存在的数据的行数
    for i in range(len(values)):
        writeSave.write(oldRowNum + 1 + i, 3, values[i][0])
        for j in range(1, len(values[i] - 1)):
            writeSave.write(oldRowNum + 1 + i, 7 + j, values[i][j])

    writeData.save(regFileName)


def GetData():
    """
    读取表格数据
    读取表格数据
    :return:
    """
    data = pda.read_excel(
        'D:/mmm/python/轨迹测试数据/0927-将文件进行分割成多个文件/新40-60002-修-2墨卡托坐标-0927-142256.xlsx')

    # data = pda.read_excel(
    #     'D:/mmm/python/轨迹测试数据/0928-分析数据特征/新40-60002-修-2墨卡托坐标-section/新40-60002-修-2墨卡托坐标==0420-1634-filed.xlsx')

    # data = pda.read_excel(
    #     'D:/mmm/python/轨迹测试数据/0928-分析数据特征/新31-Y3616_2016-10-24.xlsx')

    return data


def PlotBar():
    """
    画条形图
    :return:
    """
    # fig, axes = plt.subplots(3, 1)
    fanwei = np.arange(0, 361, 10)
    dian = np.arange(0, 10, 0.5)
    data = GetData()
    # data.loc[:, '航向'].value_counts(bins=fanwei,sort=False).plot.bar()
    data.loc[:, '点速度'].value_counts(bins=dian, sort=False).plot.bar()
    print(data.shape)

    plt.show()


def GetIndex():
    """
    获取文件的最小序列号和最大序列号
    :return:
    """
    files = askopenfilenames(title='打开文件', filetypes=[('All File', '*')])
    if files != '':
        lists = []
        df = pda.DataFrame(columns=['name', 'x', 'y'])
        for i in range(len(files)):
            # data = pda.read_excel(files[i])
            data = pda.read_csv(files[i])
            df.loc[i, 'name'] = os.path.split(files[i])[1]
            df.loc[i, 'x'] = data.loc[0,'序列号']
            df.loc[i, 'y'] = pda.to_numeric(data.序列号,errors='ignore').max()
            if df.loc[i, 'y'] == 't':
                data.drop(data.index.max(), axis=0, inplace=True)
                df.loc[i, 'y'] = pda.to_numeric(data.序列号).max()

            data.set_index('序列号',inplace=True)
            path = files[i].split('.')[0] + '.xlsx'
            data.to_excel(path)
            del data

    path = 'D:/mmm/轨迹数据集/1.xlsx'
    df.to_excel(path)
    del df


def GetInfomation():
    """
    获取文件的最小序列号和最大序列号,起止时间，有效工作点个数
    :return:
    """
    files = askopenfilenames(title='打开文件', filetypes=[('All File', '*')])
    if files != '':
        lists = []
        df = pda.DataFrame(columns=['name', 'x', 'y','轨迹点总数','工作轨迹点个数','有效轨迹点数','采样间隔','时间起','时间止','总时间'])
        for i in range(len(files)):
            # data = pda.read_excel(files[i])

            data = pda.read_csv(files[i])
            data.dropna(axis=0, how='all',inplace=True)
            df.loc[i, 'name'] = os.path.split(files[i])[1]
            df.loc[i, 'x'] = data.loc[0,'序列号']
            df.loc[i, 'y'] = pda.to_numeric(data.序列号,errors='ignore').max()
            if df.loc[i, 'y'] == 't':
                data.drop(data.index.max(), axis=0, inplace=True)
                df.loc[i, 'y'] = pda.to_numeric(data.序列号).max()

            df.loc[i,'轨迹点总数']=data.shape[0]
            df.loc[i, '工作轨迹点个数'] =sum(data.loc[:,'机具状态'])
            df.loc[i, '有效轨迹点数'] =sum(data.loc[:,'作业深度(mm)']>=data.loc[:,'达标标准深度(mm)'])
            df.loc[i, '采样间隔'] =0 #data.loc[:,'时间间隔'].mode()
            df.loc[i, '时间起'] =data.loc[0,'GPS时间']
            df.loc[i, '时间止'] =data.loc[df.loc[i, 'y']-data.loc[0,'序列号'],'GPS时间']
            df.loc[i, '总时间'] =0


            # data.set_index('序列号',inplace=True)
            # path = files[i].split('.')[0] + '.xlsx'
            # data.to_excel(path)
            del data

    path = 'D:/mmm/轨迹数据集/1.xlsx'
    df.to_excel(path)
    del df

GetInfomation()

# 第三次测试