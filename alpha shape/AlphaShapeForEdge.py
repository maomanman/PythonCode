from scipy.spatial import Delaunay
import numpy as np
from collections import defaultdict
import pandas as pda
import math as ma
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time
from ZuoBiaoZhuanHuan import LatLon2GSXY
from tkinter.filedialog import *
import sys

import tkinter as tk

import os


def alpha_shape_3D(pos, alpha):
    """
    Compute the alpha shape (concave hull) of a set of 3D points.
    Parameters:
        pos - np.array of shape (n,3) points.
        alpha - alpha value.
    return
        outer surface vertex indices, edge indices, and triangle indices
    """

    tetra = Delaunay(pos)
    # Find radius of the circumsphere.
    # By definition, radius of the sphere fitting inside the tetrahedral needs
    # to be smaller than alpha value
    # http://mathworld.wolfram.com/Circumsphere.html
    tetrapos = np.take(pos, tetra.vertices, axis=0)
    normsq = np.sum(tetrapos ** 2, axis=2)[:, :, None]
    ones = np.ones((tetrapos.shape[0], tetrapos.shape[1], 1))
    a = np.linalg.det(np.concatenate((tetrapos, ones), axis=2))
    Dx = np.linalg.det(np.concatenate((normsq, tetrapos[:, :, [1, 2]], ones), axis=2))
    Dy = -np.linalg.det(np.concatenate((normsq, tetrapos[:, :, [0, 2]], ones), axis=2))
    Dz = np.linalg.det(np.concatenate((normsq, tetrapos[:, :, [0, 1]], ones), axis=2))
    c = np.linalg.det(np.concatenate((normsq, tetrapos), axis=2))
    r = np.sqrt(Dx ** 2 + Dy ** 2 + Dz ** 2 - 4 * a * c) / (2 * np.abs(a))

    # Find tetrahedrals
    tetras = tetra.vertices[r < alpha, :]
    # triangles
    TriComb = np.array([(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)])
    Triangles = tetras[:, TriComb].reshape(-1, 3)
    Triangles = np.sort(Triangles, axis=1)
    # Remove triangles that occurs twice, because they are within shapes
    TrianglesDict = defaultdict(int)
    for tri in Triangles: TrianglesDict[tuple(tri)] += 1
    Triangles = np.array([tri for tri in TrianglesDict if TrianglesDict[tri] == 1])
    # edges
    EdgeComb = np.array([(0, 1), (0, 2), (1, 2)])
    Edges = Triangles[:, EdgeComb].reshape(-1, 2)
    Edges = np.sort(Edges, axis=1)
    Edges = np.unique(Edges, axis=0)

    Vertices = np.unique(Edges)
    return Vertices, Edges, Triangles


def distance(a, b):
    """
    计算a,b两点的直线距离
    :param a: a点坐标（大地坐标 m）
    :param b: b点坐标（大地坐标 m）
    :return: dis 直线距离
    """
    p1 = np.array(a)
    p2 = np.array(b)

    dis = ma.sqrt(sum(np.power(p2 - p1, 2)))
    return dis


def alpha_shape_2D(data, radius, plotCircleflag=0):
    """
    alpha shapes 算法检测边缘
    :param x: 原始点坐标集 x轴
    :param y: 原始点坐标集 y轴
    :param plotCircleflag:默认为0 不对alpha圆进行图像显示， =1 则画出alpha 圆
    :param radius: 圆半径
    :return: 边缘点集
    """

    x = data.x
    y = data.y
    count = len(x)
    i = 0
    temp_k = 0
    edge_x = []
    edge_y = []
    edge = []  # 存放边界点在原轨迹文件中的顺序号，非原轨迹文件中序列号
    edge_len = 0

    while (i < count):  # 遍历点集里的所有的点
        # 根据农机作业轨迹的特性（有一定规律的，一列一列的排列）
        # 筛选 以当前点为质心，边长为 4*radius 的正方形区域 内的点 ，计算这些点与当前点的连线是否构成边界
        i_range = np.array([t for t, v in enumerate(x < x[i] + 2 * radius) if v == True])
        i_range = i_range[[t for t, v in enumerate(data.loc[i_range, 'x'] > x[i] - 2 * radius) if v == True]]
        i_range = i_range[[t for t, v in enumerate(data.loc[i_range, 'y'] < y[i] + 2 * radius) if v == True]]
        i_range = i_range[[t for t, v in enumerate(data.loc[i_range, 'y'] > y[i] - 2 * radius) if v == True]]

        # 测试所用
        # if i==1:
        #     print(i)

        """ i_range 是可能与当前点的连线组成边界线的备选点集"""
        for k in i_range:
            # 避免重复选点（一个点不能组成三个边界线，最多只能组成两条边界）
            if edge_x.count(x[k]) > 0 and edge_y.count(y[k]) > 0:
                if edge_x.index(x[k]) == 0 and edge_y.index(y[k]) == 0:
                    pass
                else:
                    continue

            # 计算 当前点 与 备选点 的距离
            dis = distance((x[i], y[i]), (x[k], y[k]))

            # 因为当前点 和 备选点 要在一个圆上，所有距离不能大于圆直径, 或者 当前点 与 备选点 重合
            if dis > 2 * radius or dis == 0:
                continue

            # 当前点与备选点的连线 L 线段中点
            center_x = (x[k] + x[i]) * 0.5
            center_y = (y[k] + y[i]) * 0.5

            # L 的 方向向量
            direct_x = x[k] - x[i]
            direct_y = y[k] - y[i]

            #  L 的 法向量K 及其单位化
            nomal_x = -direct_y / ma.sqrt(pow(direct_x, 2) + pow(direct_y, 2))
            nomal_y = direct_x / ma.sqrt(pow(direct_x, 2) + pow(direct_y, 2))

            # 圆心到直线L 距离
            disOfcenter = ma.sqrt(pow(radius, 2) - 0.25 * pow(dis, 2))

            if nomal_x != 0:
                a = ma.sqrt(pow(disOfcenter, 2) / (1 + pow(nomal_y / nomal_x, 2)))
                b = a * (nomal_y / nomal_x)
            else:
                a = 0
                b = disOfcenter

            # 圆心 坐标
            cicle1_x = center_x + a
            cicle1_y = center_y + b

            cicle2_x = center_x - a
            cicle2_y = center_y - b

            # 检测圆内是否有其他点
            b1 = False
            b2 = False

            # 筛选以圆心R1为质点，边长为 2*radius 的方形区域内的点集
            inSquare = np.array([t for t, v in enumerate(x < cicle1_x + radius) if v == True])
            inSquare = inSquare[[t for t, v in enumerate(data.loc[inSquare, 'x'] > cicle1_x - radius) if v == True]]
            inSquare = inSquare[[t for t, v in enumerate(data.loc[inSquare, 'y'] < cicle1_y + radius) if v == True]]
            inSquare = inSquare[[t for t, v in enumerate(data.loc[inSquare, 'y'] > cicle1_y - radius) if v == True]]
            if len(inSquare) != 0:
                for j in inSquare:
                    if j == i or j == k or distance((x[j], y[j]), (x[i], y[i])) == 0 or distance((x[j], y[j]), (
                            x[k], y[k])) == 0:  # 点集内的点 除去当前点i 和 备选点k
                        continue
                    else:
                        d = distance((x[j], y[j]), (cicle1_x, cicle1_y))  # 计算备选点k与点集内的点的距离
                        if d <= radius:  # 圆内有点 ，跳过
                            b1 = True
                            break
            # 筛选 圆R2
            inSquare = np.array([t for t, v in enumerate(x < cicle2_x + radius) if v == True])
            inSquare = inSquare[[t for t, v in enumerate(data.loc[inSquare, 'x'] > cicle2_x - radius) if v == True]]
            inSquare = inSquare[[t for t, v in enumerate(data.loc[inSquare, 'y'] < cicle2_y + radius) if v == True]]
            inSquare = inSquare[[t for t, v in enumerate(data.loc[inSquare, 'y'] > cicle2_y - radius) if v == True]]
            if len(inSquare) != 0:
                for j in inSquare:  # 与原两个点的坐标点一样
                    if j == i or j == k or distance((x[j], y[j]), (x[i], y[i])) == 0 or distance((x[j], y[j]),
                                                                                                 (x[k], y[k])) == 0:
                        continue
                    else:
                        d = distance((x[j], y[j]), (cicle2_x, cicle2_y))
                        if d <= radius:  # 圆内有点 ，跳过
                            b2 = True
                            break

            # 圆1 或 圆2 内没有其他的点，则备选点k是边界点
            if b1 == False or b2 == False:
                if edge_x.count(x[i]) < 1 or edge_y.count(y[i]) < 1:  # 当前点未加入边界点集
                    edge_x.append(x[i])
                    edge_y.append(y[i])
                    edge.append(i)
                if edge_x.count(x[k]) < 1 or edge_y.count(y[k]) < 1:  # 备选点k已未加入边界点集
                    edge_x.append(x[k])
                    edge_y.append(y[k])
                    edge.append(k)

                # 画出圆
                if b1 == False:
                    if plotCircleflag:
                        plotCircle(cicle1_x, cicle1_y)
                elif b2 == False:
                    if plotCircleflag:
                        plotCircle(cicle2_x, cicle2_y)

                # if edge_x.index(x[k]) == 0 and edge_y.index(y[k]) == 0 :
                if edge_x.index(x[k]) == 0 and edge_y.index(y[k]) == 0:  # 边界点个数达到总
                    if edge_len - edge_x.index(x[k]) > count * 0.03:  # 边界点总数达到一定数量后才可能到达结束点
                        temp_k = count
                    else:
                        continue
                else:
                    temp_k = k
                break

        # print("edge_len={},i={}".format(edge_len,i))
        # print(i)
        if edge_len < len(edge_x) or temp_k == count:  # 跳转到新的边界点
            i = temp_k
            edge_len = len(edge_x)
        else:
            i = i + 1

        # i = i + 1
    edge_x.append(edge_x[0])
    edge_y.append(edge_y[0])
    edge.append(0)

    return edge_x, edge_y, edge


def GetData(path):
    """
    读取表格数据
    读取表格数据
    :return:
    """

    # data = pda.read_excel('D:/mmm/python/轨迹测试数据/1104-alpha shape/新40-60002_2016-04-21==0421-0315-filed.xlsx')

    # data = pda.read_csv('D:/mmm/轨迹数据集/地块/按作业模式分类/套行法/csv/皖11-2004_2016-10-04==1003-2348-field.csv')
    filetype = path.split('.')[1]
    if filetype == 'csv':
        data = pda.read_csv(path)
    else:
        data = pda.read_excel(path)

    columns = data.columns

    # if 'x' not in columns:
    #     x, y = LonLatitude2WebMercator(data.经度, data.纬度)
    #     data['x'] = x
    #     data['y'] = y

    # 全部换成高斯坐标再重新计算
    x, y = LatLon2GSXY(data.经度, data.纬度)
    data['x'] = x
    data['y'] = y
    return data


def getBatchEdge(radius=6.625):
    """
    批量获得边界点 radius=6.625最优,遍历rootpath路径下所有csv文件，并都检测边界点保存在edgePath，以及画出点及边界保存图片在imagePath
    使用方法:
    :return:
    """
    rootpath = R'D:\mmm\轨迹数据集\汇总'
    fns = (fn for fn in os.listdir(rootpath) if fn.endswith('.xls'))
    info = pda.DataFrame(columns=['filename', 'edgeNum', 'pointNum', '耗时'])
    t = 0
    for fn in fns:
        print(fn)
        path = rootpath + '/' + fn
        data = GetData(path)

        edgePath = rootpath + '/edge-GSXY-R=6625'
        if not os.path.exists(edgePath):
            os.mkdir(edgePath)
        path = edgePath + '/' + fn.split('.')[0] + '-edge'
        start = time.time()
        edge_x, edge_y, edge_index = alpha_shape_2D(data, radius)
        end = time.time()
        print('运行时间：{}'.format(end - start))

        dd = pda.DataFrame({'pointIndex': edge_index, 'x': edge_x, 'y': edge_y})

        dd.to_csv(path + '.csv')
        # dd.to_excel(path+'.xlsx')

        info.loc[t] = [fn, len(edge_x), data.shape[0], end - start]
        t = t + 1

        # imagePath = rootpath + '/image-R=6625'
        # if not os.path.exists(imagePath):
        #     os.mkdir(imagePath)
        # path = imagePath + '/' + fn.split('.')[0] + '-image.png'
        #
        # plotEdge(data.x, data.y, edge_x, edge_y, path)
        del data
    info.to_excel(rootpath + '/AllInfo-GSXY-R=6625.xlsx')
    del info


def justShowEdge(radius=6.625):
    """
    获得边界点 radius=6.625最优,并进行展示，不保存

    使用方法:
    :return:
    """

    path = r'D:\mmm\轨迹数据集\汇总\00001 耕-大-套==黑02-452C12_2016-10-9==1009-0125.xls'
    data = GetData(path)

    start = time.time()
    edge_x, edge_y, edge_index = alpha_shape_2D(data, radius)
    end = time.time()
    print('运行时间：{}'.format(end - start))

    plotEdge(data.x, data.y, edge_x, edge_y)
    del data


def plotEdge(data_x, data_y, edge_x, edge_y, path=''):
    """
    画出原始轨迹图和边界轨迹图
    :param data_x:  原始轨迹点的横坐标
    :param data_y:  原始轨迹点的纵坐标
    :param edge_x:  边界轨迹点的横坐标
    :param edge_y:  边界轨迹点的纵坐标
    :param path:    轨迹图的存放路径及名称
    :return:
    """
    # i = 0
    # while i < len(edge_x):
    #     plt.text(edge_x[i], edge_y[i], i, ha='center', va='bottom', fontsize=11, color='b')
    #     i += 1

    plt.plot(data_x, data_y, 'bo', color='k', linewidth=1, markersize=2)
    plt.plot(edge_x, edge_y, '*-', color='r', markersize=6)

    plt.axis('off')
    if path:
        plt.savefig(path)
    else:
        plt.show()
    plt.close()


def findRadius():
    """
    搜寻合适的圆半径
    :return:
    """
    path = 'D:/mmm/python/轨迹测试数据/1106-半径优化'
    f_r = '湘12-E1136_2016-10-13==1013-0746-field.csv'
    f_t = '皖17-80100_2016-10-07==1006-2357-field.csv'
    f_s = '新42-98765_2016-11-10==1109-2117-field.csv'
    imagepath_r = path + '/image/' + f_r.replace('.csv', '-image.png')
    imagepath_t = path + '/image/' + f_t.replace('.csv', '-image.png')
    imagepath_s = path + '/image/' + f_s.replace('.csv', '-image.png')
    imagepath = [imagepath_r, imagepath_t, imagepath_s]
    data_r = GetData(path + '/' + f_r)  # 绕行
    data_t = GetData(path + '/' + f_t)  # 套行
    data_s = GetData(path + '/' + f_s)  # 梭行
    datas = [data_r, data_t, data_s]
    # radius = np.linspace(1, 10, 10)  # 设置半径的选项值
    # radius = np.linspace(3, 10, 15)  # 设置半径的选项值
    # radius = np.linspace(5, 8, 16)  # 设置半径的选项值
    radius = np.linspace(5, 5.6, 13)  # 设置半径的选项值
    radiusInfo = pda.DataFrame(columns=['radius', 'edgeNum', 'pointNum', '耗时', '边界占比率'])
    i = 0
    for r in radius:
        for data, im in zip(datas, imagepath):
            start = time.time()
            edge_x, edge_y, edge_index = alpha_shape_2D(data, r)
            end = time.time()
            radiusInfo.loc[i] = [r, len(edge_x), data.shape[0], end - start, len(edge_x) / data.shape[0]]
            i += 1
            im = im.replace('.', '-' + str(r) + '.')
            plotEdge(data.x, data.y, edge_x, edge_y, im)

    radiusInfo.to_excel(path + '/radiusInfo=50-56.xlsx')
    del radiusInfo


def lenthOfRoute():
    # 计算总行程长度
    lenthOfRouteInfo = pda.DataFrame(columns=['filename', 'edgeNum', '总行程长度', '行程长度计算时间', '总作业点数', '有效作业点数', '有效作业率'])
    ai = 0
    path = 'D:/mmm/轨迹数据集/地块/按作业模式分类/just'
    fns = [fn for fn in os.listdir(path) if fn.endswith('.csv')]
    for fn in fns:
        filepath = path + '/' + fn
        data = GetData(filepath)

        count = data.shape[0] - 1
        i = 0
        lenth = 0
        # 总行程累计
        start = time.time()
        while i < count:
            lenth += distance((data.x[i], data.y[i]), (data.x[i + 1], data.y[i + 1]))
            i += 1
        end = time.time()

        # 有效作业率
        validPoint = sum(data.loc[:, '作业深度(mm)'] >= data.loc[:, '达标标准深度(mm)'])
        workPoint = sum(data.loc[:, '机具状态'] == 1)

        lenthOfRouteInfo.loc[ai] = [fn, count, lenth, end - start, workPoint, validPoint, validPoint / workPoint]
        ai += 1
        del data

    lenthOfRouteInfo.to_excel(path + '/lenthOfRouteInfo.xlsx')


def splitWorkPoint(data):
    """
    将一块地中的工作点和非工作点分开，根据工作状态属性
    :param data:  需要分割的原始轨迹文件
    :return:
    """


def plotCircle(cicle_x, cicle_y, radius=6.625):
    """
    根据圆心和半径画圆
    :param cicle_x:  圆心横坐标
    :param cicle_y:  圆心纵坐标
    :param radius:  圆半径
    :return:
    """
    cir1 = Circle(xy=(cicle_x, cicle_y), radius=radius, alpha=0.4, edgecolor='b', facecolor='None',
                  lw=2)  # 第一个参数为圆心坐标，第二个为半径 #第三个为透明度（0-1）
    ax.add_patch(cir1)
    plt.axis('scaled')
    plt.axis('equal')


def calWorkTime():
    """
    计算一块地的总作业时间
    :param data: 地块作业轨迹点
    :return: 作业总时间
    """
    fn = askopenfilenames(title='选择文件', filetypes=[('*', 'csv'), ('*', 'xls'), ('*', 'xlsx')])
    if fn:
        info=pda.DataFrame(columns=['filename','width'])
        for f in fn:
            # data = GetData(r'D:\mmm\轨迹数据集\汇总\00002 耕-大-梭==黑02-S45274_2017-9-21==0921-0313-filed.xls')
            if (f.split('.')[1] == 'csv'):
                data = pda.read_csv(f)
            else:
                data = pda.read_excel(f)
            count = data.shape[0]
            flag = 0 # 标识开始结束时间
            sumTime = pda.to_timedelta(0)
            for i in range(0, count - 1):  # range 包含 起点 不包含 终点
                if flag == 0:
                    startTime = data.loc[i, 'GPS时间']
                    # print('start：{}  {}'.format(data.loc[i, '序列号'],startTime))
                    flag = 1
                if data.loc[i + 1, '序列号'] - data.loc[i, '序列号'] == 1:  # 说明轨迹点不连续
                    if i == count - 2:
                        endTime = data.loc[i + 1, 'GPS时间']
                        # print('end：{} {}'.format(data.loc[i+1, '序列号'],endTime))
                    else:
                        continue
                else:
                    endTime = data.loc[i, 'GPS时间']
                    # print('end：{} {}'.format(data.loc[i, '序列号'],endTime))

                if type(startTime) == str:
                    startTime = pda.Timestamp(startTime)
                    endTime = pda.Timestamp(endTime)
                sumTime = sumTime + (endTime - startTime)
                flag = 0
            print(sumTime)


####################################### main ############################


# 在轨迹图上画圆需要 (plotCircle)  begin
global fig, ax
fig = plt.figure()
ax = fig.add_subplot(111)
# 在轨迹图上画圆需要 end

# getBatchEdge()
# findRadius()
# lenthOfRoute()
# justShowEdge()
calWorkTime()