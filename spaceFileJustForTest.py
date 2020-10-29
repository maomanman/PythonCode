import pandas as pda
import numpy as np
import math as ma
import turtle
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import *
import xlwt
import xlrd
from xlutils.copy import copy

import tkinter.messagebox
from tkinter.filedialog import *

from matplotlib.patches import Ellipse, Circle
import matplotlib.pyplot as plt

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
            df.loc[i, 'x'] = data.loc[0, '序列号']
            df.loc[i, 'y'] = pda.to_numeric(data.序列号, errors='ignore').max()
            if df.loc[i, 'y'] == 't':
                data.drop(data.index.max(), axis=0, inplace=True)
                df.loc[i, 'y'] = pda.to_numeric(data.序列号).max()

            data.set_index('序列号', inplace=True)
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
        df = pda.DataFrame(columns=['name', 'x', 'y', '轨迹点总数', '工作轨迹点个数', '有效轨迹点数', '采样间隔', '时间起', '时间止', '总时间'])
        for i in range(len(files)):
            # data = pda.read_excel(files[i])

            data = pda.read_csv(files[i])
            data.dropna(axis=0, how='all', inplace=True)
            df.loc[i, 'name'] = os.path.split(files[i])[1]
            df.loc[i, 'x'] = data.loc[0, '序列号']
            df.loc[i, 'y'] = pda.to_numeric(data.序列号, errors='ignore').max()
            if df.loc[i, 'y'] == 't':
                data.drop(data.index.max(), axis=0, inplace=True)
                df.loc[i, 'y'] = pda.to_numeric(data.序列号).max()

            df.loc[i, '轨迹点总数'] = data.shape[0]
            df.loc[i, '工作轨迹点个数'] = sum(data.loc[:, '机具状态'])
            df.loc[i, '有效轨迹点数'] = sum(data.loc[:, '作业深度(mm)'] >= data.loc[:, '达标标准深度(mm)'])
            df.loc[i, '采样间隔'] = 0  # data.loc[:,'时间间隔'].mode()
            df.loc[i, '时间起'] = data.loc[0, 'GPS时间']
            df.loc[i, '时间止'] = data.loc[df.loc[i, 'y'] - data.loc[0, '序列号'], 'GPS时间']
            df.loc[i, '总时间'] = 0

            # data.set_index('序列号',inplace=True)
            # path = files[i].split('.')[0] + '.xlsx'
            # data.to_excel(path)
            del data

    path = 'D:/mmm/轨迹数据集/1.xlsx'
    df.to_excel(path)
    del df


def plotTime():
    """
    绘制时序图，时间为坐标轴
    :return:
    """
    dates = ['2016010106', '2016010107', '2016010108', '2016010109', '2016010110', '2016010111', '2016010112',
             '2016010113',
             '2016010114', '2016010115', '2016010116', '2016010117', '2016010118']
    # 把string格式的日期转换成datetime格式
    xs = [datetime.strptime(d, '%Y%m%d%H') for d in dates]
    # xs = dates
    ys = ['36', '29', '26', '22', '29', '38', '48', '55', '5'
                                                          '6', '60', '55', '48', '51']

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # 指定X轴的以日期格式（带小时）显示
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H'))
    # X轴的间隔为小时
    ax.xaxis.set_major_locator(mdates.HourLocator())

    plt.plot(xs, ys)
    print(type(xs[1]))
    plt.gcf().autofmt_xdate()
    plt.show()


def plotTimeTo3D():
    """
    绘制时序图，时间为坐标轴
    :return:
    """
    # 生成横纵坐标信息
    dates = ['2016-12-19 09:52:54', '2016-12-20 15:52:54', '2016-12-20 21:52:54', '2016-12-21 03:52:54']
    zs = [datetime.strptime(m, '%Y-%m-%d %H:%M:%S') for m in dates]
    ys = range(len(zs))
    xs = range(len(zs))

    print(xs)
    print(ys)
    # 配置横坐标
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    # Plot
    print(type(xs[1]))
    print(type(ys[1]))
    print(type(zs[1]))
    ax.plot(xs, ys, xs)

    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.show()


def plotLine():
    """
    给定点坐标，将其画成线
    :return:
    """
    x = [9268280.511, 9268277.914, 9268275.761, 9268272.441, 9268269.398, 9268266.188, 9268266.819, 9268269.324,
         9268271.662, 9268273.832, 9268275.41, 9268276.819, 9268276.746, 9268276.541, 9268277.692, 9268279.695]
    y = [5866142.382, 5866138.552, 5866135.747, 5866133.077, 5866130.084, 5866129.733, 5866129.814, 5866129.543,
         5866128.843, 5866127.763, 5866125.715, 5866123.179, 5866123.611, 5866127.925, 5866130.838, 5866133.32]
    lon = [83.2550195, 83.25499617, 83.25497683, 83.254947, 83.25491967, 83.25489083, 83.2548965, 83.254919, 83.25494,
           83.2549595, 83.25497367, 83.25498633, 83.25498567, 83.25498383, 83.25499417, 83.25501217]
    lat = [46.53204567, 46.532022, 46.53200467, 46.53198817, 46.53196967, 46.5319675, 46.531968, 46.53196633, 46.531962,
           46.53195533, 46.53194267, 46.531927, 46.53192967, 46.53195633, 46.53197433, 46.53198967]

    " 这一段是标记每个点的坐标"
    # i=0
    # while i <len(x):
    #     plt.text(x[i],y[i],(lon[i],lat[i]),ha='center',va='bottom',fontsize=8,color='b')
    #     i+=1
    "结束"

    plt.axis('off')
    plt.plot(x, y, 'bo-', color='k', linewidth=2, markersize=6, markerfacecolor='r', markeredgecolor='r')

    # plt.savefig("D:/mmm/python/轨迹测试数据/0928-分析数据特征/point+line.jpg")
    plt.show()


def distenceCompare():
    """
    两种用经纬度计算距离的公式比较
    :return:
    """
    lat1 = 83.2550195
    lon1 = 46.53204567
    lat2 = 83.25499617
    lon2 = 46.532022
    "第一种 从百度得"
    distence = 0
    temp = ma.sin(lat1) * ma.sin(lat2) * ma.cos(lon1 - lon2) + ma.cos(lat1) * ma.cos(lat2)
    if temp > 1 or temp < -1:
        # print('i = {},temp = {}'.format(i,temp))
        if lon1 == lon2 and lat1 == lat2:
            distence = 0
    else:
        distence = 6371004 * ma.acos(temp) * ma.pi / 180.0

    print('第一种 d={}米'.format(distence))

    tem = ma.cos(lat1) * ma.cos(lat2) * (ma.cos(lon1) * ma.cos(lon2) + ma.sin(lon1) * ma.sin(lon2)) + ma.sin(
        lat1) * ma.sin(lat2)
    distence2 = 6371004 * ma.acos(tem) * ma.pi / 180.0
    print('第2.0种 acos(tem)={}'.format(ma.acos(tem)))
    print('第2种 d={}米'.format(distence2))

def plotParallelLine():
    """
    绘制平行线
    :return:
    """

    # turtle.penup()
    # turtle.goto(100, 100)
    # turtle.pendown()
    #
    # turtle.forward(100)
    # turtle.left(90)
    # turtle.forward(200)
    #
    # turtle.penup()
    # turtle.goto(100,100)
    # turtle.pendown()
    # turtle.forward(100)
    #
    # turtle.penup()
    # turtle.goto(100,200)
    # turtle.pendown()
    # turtle.forward(100)
    #
    # turtle.penup()
    # turtle.goto(100,300)
    # turtle.pendown()
    # turtle.forward(100)
    #
    # turtle.done()

    turtle.title('数据驱动的动态路径绘制')  # 建立的窗口标题

    turtle.setup(800, 600, 0, 0)  # 建立的窗口大小及位置

    # 设置画笔

    pen = turtle.Turtle()  # 创建一个画笔实例

    pen.color("red")  # 初始化颜色为红色

    pen.width(5)  # 线条宽度为5px

    pen.shape("turtle")  # 初始化画笔形状

    pen.speed(10)  # 海龟速度

    # pen.fillcolor("blue")

    # pen.begin_fill()

    # 读取文件

    result = []  # 创建一个列表

    file = open("data.txt", "r")  # 打开提前设置好的数据文件

    for line in file:  # 遍历之

        result.append(list(map(float, line.split(','))))  # 每循环一次把后面一行的数据加到result忠

    print(result)  # 打印之

    # 动态绘制

    for i in range(len(result)):  # len()指的是列表数据长度

        pen.color((result[i][3], result[i][4], result[i][5]))  # 随着数据的变化线条颜色变化

        pen.forward(result[i][0])  # 小乌龟运动方向

        if result[i][1]:

            pen.rt(result[i][2])

            # pen.fill(Ture)

        else:

            pen.lt(result[i][2])

    pen.goto(0, 0)

    # x = [0, 7]
    # y = [5, 2]
    # plt.plot(x, y)
    #
    # o = np.subtract(2, 5)
    # q = np.subtract(7, 0)
    # slope = o / q
    #
    # # (m,p) are the new coordinates to plot the parallel line
    # m = 3
    # p = 2
    #
    # axes = plt.gca()
    # x_val = np.array(axes.get_xlim())
    # y_val = np.array(slope * (x_val - m) + p)
    # plt.plot(x_val, y_val, color="black", linestyle="--")
    # plt.show()

def plotOverlap():
    """
    画曲线重叠区域的阴影
    :return:
    """
    x = np.linspace(0, 10)
    y = (x - 3) * (x - 5) * (x - 7) + 85
    y1 = 60-x

    # 画线
    fig, ax = plt.subplots()
    plt.plot(x, y, 'r', linewidth=2)
    plt.plot(x, y1, 'g', linewidth=2)
    plt.ylim(ymin=0)

    # 画阴影区域
    a, b = 2, 9  # integral limits
    xf = x[np.where((x > a) & (x < b))]
    # plt.fill_between(xf),在xf范围内
    # 曲线1：np.zeros(len(xf))与曲线2：func(xf)之间的区域
    # np.zeros()从零开始，np.ones()从1开始，np.ones()*20从20开始
    # plt.fill_between(xf, np.zeros(len(xf)), func(xf), color='blue', alpha=.25)
    # 两条曲线之间的区域
    plt.fill_between(xf, 60-xf, (xf - 3) * (xf - 5) * (xf - 7) + 85, color='blue', alpha=0.25)
    plt.show()


def plotCircle(cicle1_x,cicle1_y,cicle2_x,cicle2_y,radius):
    """
    用于alpha shape 算法画圆的
    :return:
    """
    # from matplotlib.patches import Ellipse, Circle
    # import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111)
    cir1 = Circle(xy=(cicle1_x, cicle1_y), radius=radius, alpha=0.2, color='g')  # 第一个参数为圆心坐标，第二个为半径 #第三个为透明度（0-1）
    ax.add_patch(cir1)
    plt.axis('scaled')
    plt.axis('equal')
    cir2 = Circle(xy=(cicle2_x, cicle2_y), radius=radius, alpha=0.2)
    ax.add_patch(cir2)

    plt.plot(x[591], y[591], 'co', color='c')
    # plt.plot(x[i_range],y[i_range],'co',color='r')
    plt.plot([x[i], x[k]], [y[i], y[k]], '*')
    plt.plot([cicle1_x, cicle2_x], [cicle1_y, cicle2_y], 'bo', markerfacecolor='r')


"""
main 开始处
"""
# plotLine()
# distenceCompare()
plotParallelLine()

# plotOverlap()

tes=i_range>i
rope =[]
for t in range(len(i_range)):
    if tes[t]==True:
        rope.append(t)