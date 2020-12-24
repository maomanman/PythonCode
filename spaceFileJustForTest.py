import pandas as pda
import numpy as np
import math as ma
import turtle
from datetime import datetime
import matplotlib.dates as mdates
from mpl_toolkits.mplot3d import *
import xlwt
import xlrd
from xlutils.copy import copy

import tkinter.messagebox
from tkinter.filedialog import *

from matplotlib.patches import Ellipse, Circle
import matplotlib.pyplot as plt

from osgeo import gdal, osr
# import gdal
from osgeo.gdalconst import *


import rasterio
import json
from rasterio.mask import mask

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


def shange():
    # 栅格数据投影转换
    # from osgeo import gdal, osr
    # from osgeo.gdalconst import *
    # 源图像投影
    source = osr.SpatialReference()
    source.ImportFromEPSG(32650)
    # 目标图像投影
    target = osr.SpatialReference()
    target.ImportFromEPSG(3857)
    coordTrans = osr.CoordinateTransformation(source, target)
    # 打开源图像文件
    ds = gdal.Open("fdem.tif")
    # 仿射矩阵六参数
    mat = ds.GetGeoTransform()
    # 源图像的左上角与右下角像素，在目标图像中的坐标
    (ulx, uly, ulz) = coordTrans.TransformPoint(mat[0], mat[3])
    (lrx, lry, lrz) = coordTrans.TransformPoint(mat[0] + mat[1] * ds.RasterXSize, mat[3] + mat[5] * ds.RasterYSize)
    # 创建目标图像文件（空白图像），行列数、波段数以及数值类型仍等同原图像
    driver = gdal.GetDriverByName("GTiff")
    ts = driver.Create("fdem_lonlat.tif", ds.RasterXSize, ds.RasterYSize, 1, GDT_UInt16)
    # 转换后图像的分辨率
    resolution = (int)((lrx - ulx) / ds.RasterXSize)
    # 转换后图像的六个放射变换参数
    mat2 = [ulx, resolution, 0, uly, 0, -resolution]
    ts.SetGeoTransform(mat2)
    ts.SetProjection(target.ExportToWkt())
    # 投影转换后需要做重采样
    gdal.ReprojectImage(ds, ts, source.ExportToWkt(), target.ExportToWkt(), gdal.GRA_Bilinear)
    # 关闭
    ds = None
    ts = None

def grid():
    """
    矩形叠加栅格
    :return:
    """
    sg = np.zeros((10,10)) #栅格大小
    polygon =np.array([(1.5,4.2),(4.1,5.1),(5.9,2.5),(3.6,1.6)])# 四边形的四个顶点
    # 顶点坐标转换为栅格坐标
    sg_polygon = polygon.copy()
    sg_polygon[:,1] = 10 - sg_polygon[:,1]
    sg_polygon[:,0] = sg_polygon[:,1]
    sg_polygon[:, 1] = polygon[:,0]

    # 标记顶点
    for p in sg_polygon:
        p = np.int8(np.floor(p))
        sg[p[0],p[1]] = 1


    # 标记边界
    # i = 0
    # while i<4:
    #     if i == 3:
    #         t= 0
    #     else:
    #         t = i +1
    #     # 每条边的斜率
    #     k = (sg_polygon[t,1] - sg_polygon[i,1] ) / (sg_polygon[t,0] - sg_polygon[i,0] )

    # 标记矩形内部
    aa = sg_polygon[:,0]
    aa.sort()
    bb = sg_polygon[:,1]
    bb.sort()
    x_t = np.int8(np.floor(aa[1:3]))
    x = np.arange(x_t[0], x_t[1] + 1, 1)
    y_t = np.int8(np.floor(bb[1:3]))
    y = np.arange(y_t[0], y_t[1] + 1, 1)
    for x_i in x:
        for y_i in y:
            if sg[x_i,y_i] ==0 :
                sg[x_i, y_i] = 2

    pltp = polygon.copy()
    pltp=np.vstack([pltp,polygon[0]])
    plt.plot(pltp[:,0],pltp[:,1])
    plt.yticks(ticks=np.arange(0,11,1))
    plt.xticks(ticks=np.arange(0, 11, 1))
    plt.grid()

# def TestShanGeData():
# -*- coding: utf-8 -*-
# import rasterio
# import json
# from rasterio.mask import mask

def Clip(Tiff, Geodata):
    rasterfile = Tiff
    geoms = json.loads(Geodata)  # 解析string格式的geojson数据
    rasterdata = rasterio.open(rasterfile)
    member = 0.0  # 记录总人数
    Gridnumber = 0  # 记录相交区域总像素点数
    Transform = rasterdata._transform  # 得到影像六参数

    for i in range(len(geoms['features'])):
        geo = [geoms['features'][i]['geometry']]
        # 掩模得到相交区域
        out_image, out_transform = mask(rasterdata, geo, all_touched=True, crop=True, nodata=rasterdata.nodata)
        out_list = out_image.tolist()
        out_list = out_list[0]

        for k in range(len(out_list)):
            for j in range(len(out_list[k])):
                if out_list[k][j] >= 0:
                    member += out_list[k][j]
                    Gridnumber += 1

    # 人数单位为万人，小数点后保留两位
    print(round(member / 2500, 2))
    # 面积单位为平方公里，小数点后保留两位
    print(round(Gridnumber * Transform[0] * Transform[3] / 250000, 2))

if __name__ == '__main__':
    geojson = "{\"type\":\"FeatureCollection\",\"features\":[{\"type\":\"Feature\",\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[114.4,21.2],[118.25777710514137,21.2],[118.25890798273747,21.299120898984143],[118.25711853337589,21.398166452889882],[118.25240412231551,21.49706137436084],[118.24476226308434,21.59573049143711],[118.23419263830453,21.694098805135695],[118.22069711944573,21.792091546888855],[118.20427978543194,21.88963423579395],[118.1849469400189,21.98665273562841],[118.16270712785808,22.08307331158244],[118.13757114915893,22.178822686664432],[118.10955207286088,22.27382809773303],[118.07866524822043,22.368017351110097],[118.04492831472203,22.461318877731173],[118.00836121021473,22.553661787787973],[117.96898617717864,22.644975924820585],[117.926827767026,22.735191919215197],[117.88191284233778,22.82424124106683],[117.83427057694053,22.912056252364096],[117.78393245372968,22.998570258456652],[117.73093226014316,23.083717558764647],[117.67530608119807,23.1674334966915],[117.6170922900003,23.24965450870252],[117.55633153564213,23.330318172531292],[117.49306672840999,23.409363254478194],[117.42734302222539,23.48672975576602],[117.35920779424919,23.562358957917922],[117.28871062158521,23.636193467125167],[117.21590325502609,23.708177257571663],[117.1408395897904,23.77825571368504],[117.06357563320853,23.846375671283738],[116.98416946932252,23.912485457590833],[116.90268122037355,23.97653493008744],[116.81917300516056,24.038475514178003],[116.73370889426224,24.09826023964223],[116.64635486212364,24.155843775848723],[116.55717873602077,24.211182465706713],[116.46625014192614,24.264234358333454],[116.373640447306,24.314959240415533],[116.27942270089693,24.36331866624397],[116.18367156951217,24.409275986403543],[116.08646327194742,24.45279637509782],[115.98787551005853,24.49384685609334],[115.88798739710091,24.53239632726536],[115.78687938342739,24.56841558373185],[115.68463317965143,24.601877339558882],[115.58133167739447,24.632756248027192],[115.47705886774554,24.661028920444664],[115.37189975756928,24.686673943495634],[115.26594028380782,24.70967189511566],[115.15926722593179,24.73000535888241],[115.05196811670135,24.747658936914036],[114.94413115140696,24.762619261268355],[114.83584509576394,24.774875003835064],[114.72719919264455,24.784416884715597],[114.6182830678307,24.791237679086407],[114.50918663498032,24.795332222540992],[114.40000000000009,24.796697414907612],[114.4,21.2]]]},\"properties\":null},{\"type\":\"Feature\",\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[114.4,21.2],[114.40000000000009,18.50228308467689],[114.47839318760532,18.503307199671838],[114.55672962365122,18.506378768250386],[114.63495259319666,18.511495461774075],[114.71300545451652,18.518653401114477],[114.79083167565796,18.52784715955488],[114.8683748709343,18.53906976685056],[114.9455788373358,18.552312714444042],[115.022387590839,18.567565961832713],[115.09874540259307,18.58481794408408],[115.17459683496372,18.60405558049382],[115.24988677741851,18.62526428438133],[115.32456048223082,18.648427974015192],[115.39856359998942,18.673529084662846],[115.47184221489294,18.7005485817549],[115.54434287981474,18.729465975156472],[115.61601265112176,18.760259334534908],[115.68679912323262,18.79290530581477],[115.75665046289964,18.827379128707662],[115.82551544320313,18.863654655305822],[115.89334347724332,18.901704369726474],[115.96008465151897,18.94149940879379],[116.0256897589802,18.983009583743524],[116.09011033174647,19.02620340293629],[116.15329867347828,19.07104809556239],[116.21520789139402,19.11750963632312],[116.27579192792268,19.165552771070054],[116.33500559198546,19.215141043384506],[116.3928045898956,19.266236822078668],[116.44914555587411,19.318801329598273],[116.5039860821679,19.37279467130668],[116.55728474876958,19.428175865629328],[116.6090011527283,19.484902875036482],[116.65909593704691,19.54293263784183],[116.70753081915825,19.602221100793372],[116.75426861897427,19.662723252433352],[116.79927328650058,19.724393157201348],[116.84250992900877,19.78718399025621],[116.88394483776051,19.851048072990466],[116.92354551427263,19.915936909210018],[116.96128069611666,19.981801221953162],[116.99712038224084,20.04859099091908],[117.03103585780605,20.11625549047926],[117.06299971852206,20.184743328241552],[117.09298589447349,20.254002484137857],[117.12096967341938,20.323980350004945],[117.14692772355352,20.394623769628254],[117.17083811570683,20.465879079217302],[117.19268034497554,20.53769214828128],[117.21243535175506,20.610008420873214],[117.23008554215835,20.682772957169675],[117.24561480779653,20.755930475354717],[117.25900854489805,20.829425393773647],[117.27025367273882,20.903201873324804],[117.27933865135765,20.977203860054487],[117.2862534985261,21.051375127922938],[117.29098980594381,21.125659321706053],[117.29354075462402,21.19999999999999],[114.4,21.2]]]},\"properties\":null},{\"type\":\"Feature\",\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[114.4,21.2],[111.50645924537594,21.19999999999999],[111.50901019405615,21.125659321706053],[111.51374650147397,21.051375127922938],[111.52066134864242,20.977203860054487],[111.52974632726114,20.903201873324804],[111.5409914551019,20.829425393773647],[111.55438519220343,20.755930475354717],[111.56991445784172,20.682772957169675],[111.587564648245,20.610008420873214],[111.60731965502441,20.53769214828128],[111.62916188429313,20.465879079217302],[111.65307227644644,20.394623769628254],[111.67903032658069,20.323980350004945],[111.70701410552658,20.254002484137857],[111.737000281478,20.184743328241552],[111.76896414219402,20.11625549047926],[111.80287961775912,20.04859099091908],[111.83871930388341,19.981801221953162],[111.87645448572744,19.915936909210018],[111.91605516223956,19.851048072990466],[111.9574900709913,19.787183990256267],[112.00072671349949,19.724393157201348],[112.04573138102569,19.662723252433352],[112.09246918084182,19.602221100793372],[112.14090406295315,19.54293263784183],[112.19099884727166,19.484902875036482],[112.24271525123038,19.428175865629328],[112.29601391783206,19.37279467130668],[112.35085444412584,19.318801329598273],[112.40719541010435,19.266236822078668],[112.46499440801472,19.215141043384506],[112.52420807207727,19.165552771070054],[112.58479210860605,19.11750963632312],[112.64670132652168,19.07104809556239],[112.70988966825348,19.02620340293629],[112.77431024101975,18.983009583743524],[112.83991534848099,18.94149940879379],[112.90665652275675,18.901704369726474],[112.97448455679694,18.863654655305822],[113.04334953710043,18.827379128707662],[113.11320087676745,18.79290530581477],[113.18398734887819,18.760259334534908],[113.25565712018533,18.729465975156472],[113.32815778510712,18.7005485817549],[113.40143640001065,18.673529084662846],[113.47543951776925,18.648427974015192],[113.55011322258156,18.62526428438133],[113.62540316503623,18.60405558049382],[113.701254597407,18.58481794408408],[113.77761240916095,18.567565961832713],[113.85442116266427,18.552312714444042],[113.93162512906565,18.53906976685056],[114.009168324342,18.52784715955488],[114.08699454548355,18.518653401114477],[114.16504740680341,18.511495461774075],[114.24327037634885,18.506378768250386],[114.32160681239475,18.503307199671838],[114.40000000000009,18.50228308467689],[114.4,21.2]]]},\"properties\":null},{\"type\":\"Feature\",\"geometry\":{\"type\":\"Polygon\",\"coordinates\":[[[114.4,21.2],[114.40000000000009,23.448160895495334],[114.33247352966828,23.447307394069753],[114.26500097353119,23.444747537182025],[114.19763619552975,23.44048326651341],[114.13043295917385,23.434517816577568],[114.06344487751585,23.42685571229009],[113.99672536335152,23.41750276556752],[113.93032757972082,23.406466070958686],[113.86430439078458,23.39375400031156],[113.7987083131469,23.379376196479143],[113.7335914676953,23.363343566068465],[113.66900553202856,23.345668271238367],[113.60500169353759,23.326363720550944],[113.54163060320673,23.30544455888355],[113.47894233019758,23.282926656408677],[113.41698631727627,23.258827096647906],[113.35581133714209,23.23316416361058],[113.29546544971413,23.205957328023942],[113.23599596042686,23.177227232665985],[113.17744937958537,23.14699567681066],[113.11987138282689,23.115285599796152],[113.0633067727324,23.08212106372895],[113.0077994416265,23.047527235334712],[112.95339233560537,23.011530366969794],[112.90012741982423,22.97415777680635],[112.84804564507613,22.93543782820609],[112.79718691568678,22.895399908296383],[112.74759005875148,22.854074405765346],[112.69929279473217,22.81149268789119],[112.65233170943259,22.76768707682311],[112.60674222736463,22.722690825130428],[112.56255858651605,22.676538090638587],[112.51981381452674,22.629263910570103],[112.47853970627853,22.58090417500955],[112.43876680289759,22.531495599712457],[112.40052437217025,22.481075698278232],[112.36384039036511,22.429682753707652],[112.32874152545742,22.377355789366675],[112.29525312174269,22.32413453937818],[112.26339918583005,22.270059418463347],[112.23320237400071,22.21517149125674],[112.20468398091452,22.15951244111716],[112.17786392964763,22.103124538458587],[112.15276076304008,22.046050608625364],[112.12939163633348,21.988333999335737],[112.10777231107431,21.93001854771967],[112.08791715026041,21.87114854697478],[112.0698391147032,21.8117687126678],[112.05354976058175,21.75192414870628],[112.03905923816069,21.69166031300722],[112.02637629164292,21.631022982889874],[112.01550826013147,21.570058220218527],[112.00646107967054,21.508812336323217],[111.99923928633655,21.447331856725555],[111.99384602035161,21.38566348569634],[111.99028303118871,21.323854070674486],[111.98855068364242,21.26195056657275],[111.98864796483326,21.19999999999999],[114.4,21.2]]]},\"properties\":null}]}"
    Clip("E:\Workspaces\GuangDongRe.tif",geojson)










"""
main 开始处
"""
# plotLine()
# distenceCompare()
plotParallelLine()

# plotOverlap()


