from scipy.spatial import Delaunay
import numpy as np
from collections import defaultdict
import pandas as pda
import math as ma
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time
from alpha_shape.ZuoBiaoZhuanHuan import LatLon2GSXY
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


def orderRange(x, y, i, i_range, radius):
    t = np.abs(np.power(x[i_range] - x[i], 2) + np.power(y[i_range] - y[i], 2) - np.power(radius, 2))
    return list(t.sort_values().index)


def alpha_shape_2D(data, radius, plotCircleflag=0):
    """
    alpha shapes 算法检测边缘
    :param x: 原始点坐标集 x轴
    :param y: 原始点坐标集 y轴
    :param plotCircleflag:默认为0 不对alpha圆进行图像显示， =1 则画出alpha 圆
    :param radius: 圆半径
    :return: 边缘点集
    """
    data = data[data['工作状态'] == True]
    data.reset_index(drop=True, inplace=True)

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

        # i_range =  orderRange(x,y,i,i_range,radius)

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
                        plotCircle(cicle1_x, cicle1_y, radius)
                elif b2 == False:
                    if plotCircleflag:
                        plotCircle(cicle2_x, cicle2_y, radius)

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

    if edge_x != [] or edge_y != []:
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

    # 筛选 作业状态中的点
    # data=data[data['工作状态']==True]
    # data.reset_index(drop=True,inplace=True)

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


def justShowEdge(path, radius=6.625):
    """
    获得边界点 radius=6.625最优,并进行展示，不保存

    使用方法:
    :return:
    """

    data = GetData(path)

    start = time.time()
    edge_x, edge_y, edge_index = alpha_shape_2D(data, radius)
    end = time.time()
    print('运行时间：{:.2f} s'.format(end - start))

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

    plt.plot(data_x, data_y, 'bo-', color='k', linewidth=1, markersize=2)
    plt.plot(edge_x, edge_y, '*-', color='r', markersize=6)
    # plt.axis('equal')  # 通过更改轴限制设置相等的缩放比例（即，使圆成为圆形）

    plt.axis('off')
    if path:
        plt.savefig(path)
    else:
        plt.show()
    plt.close()


def filesWithDifferentWidth(index_file_path):
    """
    根据轨迹索引文件表 找出 各个幅宽不同的，且相同幅宽中轨迹点最少的文件，
    indexFilePath:轨迹索引文件的路径 'D:\mmm\轨迹数据集\轨迹索引-v1.0.xlsx'
    :return:返回DataFrame(columns=['文件名称', '幅宽', '轨迹点个数'])
    """
    file_path = 'D:\mmm\轨迹数据集\汇总'
    index_file_data = pda.read_excel(index_file_path)  # 读取索引文件
    index_file_data.rename(columns={'幅宽\n（米）': "幅宽"}, inplace=True)
    index_file_data.sort_values(by=['幅宽', '轨迹点个数'], inplace=True)  # 根据幅宽排序（按幅宽从小到大排序）
    index_file_data.reset_index(inplace=True)
    return_info = pda.DataFrame(columns=['文件名称', '幅宽', '轨迹点个数'])

    start = 0  # 列标签占据2行
    end = index_file_data.shape[0]
    j = 0
    # # 每个幅宽中选择 轨迹点最少的文件 begin
    # for i in range(start, end):  # 循环查看文件
    #     width = index_file_data.loc[i, '幅宽']
    #     if i == start:
    #         return_info.loc[j] = [index_file_data.loc[i, '文件名称'], index_file_data.loc[i, '幅宽'],
    #                               index_file_data.loc[i, '轨迹点个数']]
    #         j = j + 1
    #     elif width != index_file_data.loc[i - 1, '幅宽']:
    #         return_info.loc[j] = [index_file_data.loc[i, '文件名称'], index_file_data.loc[i, '幅宽'],
    #                               index_file_data.loc[i, '轨迹点个数']]
    #         j = j + 1
    # # 每个幅宽中选择 轨迹点最少的文件 end

    # # 每个幅宽中选择 轨迹点个数居中的文件 begin
    # i = start
    # while(i < end-1):  # 循环查看文件
    #     width = index_file_data.loc[i, '幅宽']
    #     points = index_file_data[index_file_data.幅宽 == width].轨迹点个数
    #     temp = points.reset_index(drop=True)
    #     midpoint = temp[np.floor((points.count() - 1) / 2)]
    #     midpointindex = points[points.values == midpoint].index
    #     return_info.loc[j] = [index_file_data.loc[midpointindex, '文件名称'].values[0], index_file_data.loc[midpointindex, '幅宽'].values[0],
    #                           index_file_data.loc[midpointindex, '轨迹点个数'].values[0]]
    #     j = j + 1
    #     i = i + points.count()
    # # 每个幅宽中选择 轨迹点个数居中的文件 end

    # 每个幅宽中选择 轨迹点个数最多的文件 begin
    # i = start
    # while(i < end-1):  # 循环查看文件
    #     width = index_file_data.loc[i, '幅宽']
    #     points = index_file_data[index_file_data.幅宽 == width].轨迹点个数
    #     temp = points.reset_index(drop=True)
    #     # midpoint = temp[np.floor((points.count() - 1) / 2)]
    #     maxpoint=points.max()
    #     maxpointindex = points[points.values == maxpoint].index
    #
    #     return_info.loc[j] = [index_file_data.loc[maxpointindex, '文件名称'].values[0], index_file_data.loc[maxpointindex, '幅宽'].values[0],
    #                           index_file_data.loc[maxpointindex, '轨迹点个数'].values[0]]
    #     j = j + 1
    #     i = i + points.count()
    # 每个幅宽中选择 轨迹点个数最多的文件 end

    #  同一个幅宽下的全量轨迹文件 begin
    return_info = index_file_data[['文件名称', '幅宽', '轨迹点个数']].copy()

    #  同一个幅宽下的全量轨迹文件 end

    return_info.dropna(inplace=True)  # 值缺失行丢弃
    # return_info.to_excel(r'D:\mmm\轨迹数据集\return_info.xlsx')
    return return_info


def findRadiusFromDifferentWidth():
    # 找出每个幅宽下轨迹点最少的轨迹文件
    files_data = filesWithDifferentWidth('D:\mmm\轨迹数据集\轨迹索引-v1.0.xlsx')
    path = 'D:\mmm\轨迹数据集'
    radata = pda.read_excel(r'D:\mmm\轨迹数据集\image-居中轨迹点文件\widthInfo.xlsx')

    for f, w, a in zip(files_data.loc[:, '文件名称'], files_data.loc[:, '幅宽'], radata.loc[:, '居中轨迹点的最优半径']):
        imagepath = path + '\\image\\width-' + str(w).replace('.', '-')
        imagefile = f.split(' ')
        imagefile[1] = '-image.png'
        imagefile = ''.join(imagefile)
        imagefilepath = imagepath + '\\' + imagefile
        # print(imagefilepath)
        if not os.path.exists(imagepath):
            os.makedirs(imagepath)
            print("[{}]创建成功 ".format(imagepath))

        data = GetData('D:\mmm\轨迹数据集\汇总\\' + f)

        # a=2
        if a > 10:
            radius = np.round(np.arange(a, 20.1, 0.2), 2)  # 设置半径的选项值
        else:
            radius = np.round(np.arange(a, 10, 0.2), 2)  # 设置半径的选项值
        # radius = np.round(np.arange(0.2, 10.1, 0.2), 2)  # 设置半径的选项值
        radiusInfo = pda.DataFrame(columns=['radius', 'pointNum', 'edgeNum', '边界点检测耗时(s)', '地块面积（平方米）', '面积计算耗时(s)'])
        i = 0
        for r in radius:
            imagefilepath_r = imagefilepath
            start = time.time()
            edge_x, edge_y, edge_index = alpha_shape_2D(data, r)
            end = time.time()

            area, times = calFiledArea([edge_x, edge_y])  # 根据检测出的边界点计算面积
            radiusInfo.loc[i] = [r, data.shape[0], len(edge_x), round(end - start, 2), area, times]
            i += 1
            imagefilepath_r = imagefilepath_r.replace('.', '-' + str(r) + '.')
            plotEdge(data.x, data.y, edge_x, edge_y, imagefilepath_r)
        radiusInfo.to_excel(path + '/image/radiusInfo' + str(w) + '.xlsx')
        print("幅宽[{}]画图完成 ".format(w))
        del radiusInfo
        del data
    files_data.to_excel('D:\mmm\轨迹数据集\\widthInfo.xlsx')


def findRadiusFromSameWidth():
    # 找出每个幅宽下轨迹点最少的轨迹文件
    files_data = filesWithDifferentWidth('D:\mmm\轨迹数据集\轨迹索引-v1.0.xlsx')
    path = 'D:\mmm\轨迹数据集'
    # radata=pda.read_excel(r'D:\mmm\轨迹数据集\image-居中轨迹点文件\widthInfo.xlsx')

    w = files_data.loc[1, '幅宽']
    imagepath1 = path + '\\image\\' + str(w).replace('.', '-')
    count = files_data[files_data.幅宽 == w].shape[0]
    t = 0
    for f in files_data.loc[0:count - 1, '文件名称']:
        a = 2
        # if a > 10:
        #     radius = np.round(np.arange(a, 20.1, 0.2), 2)  # 设置半径的选项值
        # else:
        #     radius = np.round(np.arange(a, 10.1, 0.2), 2)  # 设置半径的选项值
        radius = np.round(np.arange(a, 10.1, 0.2), 2)  # 设置半径的选项值
        imagepath = imagepath1 + '_num_' + str(t)

        imagefile = f.split(' ')
        imagefile[1] = '-image.png'
        imagefile = ''.join(imagefile)
        imagefilepath = imagepath + '\\' + imagefile
        # print(imagefilepath)
        if not os.path.exists(imagepath):
            os.makedirs(imagepath)
            print("[{}]创建成功 ".format(imagepath))

        data = GetData('D:\mmm\轨迹数据集\汇总\\' + f)

        radiusInfo = pda.DataFrame(columns=['radius', 'pointNum', 'edgeNum', '边界点检测耗时(s)', '地块面积（平方米）', '面积计算耗时(s)'])
        i = 0
        for r in radius:
            imagefilepath_r = imagefilepath
            start = time.time()
            edge_x, edge_y, edge_index = alpha_shape_2D(data, r)
            end = time.time()

            area, times = calFiledArea([edge_x, edge_y])  # 根据检测出的边界点计算面积
            radiusInfo.loc[i] = [r, data.shape[0], len(edge_x), round(end - start, 2), area, times]
            i += 1
            imagefilepath_r = imagefilepath_r.replace('.', '-' + str(r) + '.')
            plotEdge(data.x, data.y, edge_x, edge_y, imagefilepath_r)
        radiusInfo.to_excel(path + '/image/radiusInfo_' + str(t) + '.xlsx')
        t = t + 1
        print("幅宽[{}]画图完成 ".format(w))
        del radiusInfo
        del data
    files_data.to_excel('D:\mmm\轨迹数据集\\image\widthInfo.xlsx')


def test7():
    # 找出每个幅宽下轨迹点最少的轨迹文件
    # files_data = filesWithDifferentWidth('D:\mmm\轨迹数据集\轨迹索引-v1.0.xlsx')
    files_data = pda.read_excel('D:\\mmm\\轨迹数据集\\image-test6-2\\edgeInfo1-4.xlsx')
    path = 'D:\mmm\轨迹数据集\\test7\\'
    # radata=pda.read_excel(r'D:\mmm\轨迹数据集\image-居中轨迹点文件\widthInfo.xlsx')

    count = files_data[files_data.边界是否完整 != '是'].shape[0]
    t = 0
    for f in files_data.loc[0:count - 1, '文件名']:
        a = 3.8
        radius = np.round(np.arange(a, 10.1, 0.2), 2)  # 设置半径的选项值
        imagepath = path + str(t) + '_num_' + f.split(' ')[0]
        if not os.path.exists(imagepath):
            os.makedirs(imagepath)
            print("[{}]创建成功 ".format(imagepath))

        data = GetData('D:\mmm\轨迹数据集\汇总\\' + f)

        # 边界图片命名
        imagefile = f.split(' ')
        imagefile[1] = '-image.png'
        imagefile = ''.join(imagefile)
        imagefilepath = imagepath + '\\' + imagefile
        # print(imagefilepath)
        radiusInfo = pda.DataFrame(
            columns=['radius', 'pointNum', 'edgeNum', '边界点检测耗时(s)', '地块面积（平方米）', '面积计算耗时(s)'])

        i = 0
        for r in radius:
            imagefilepath_r = imagefilepath
            # 边界检测
            start = time.time()
            edge_x, edge_y, edge_index = alpha_shape_2D(data, r)
            end = time.time()
            # 面积计算
            area, times = calFiledArea([edge_x, edge_y])  # 根据检测出的边界点计算面积
            # 登记
            radiusInfo.loc[i] = [r, data.shape[0], len(edge_x), round(end - start, 2), area, times]
            i += 1
            imagefilepath_r = imagefilepath_r.replace('.', '-' + str(r) + '.')
            plotEdge(data.x, data.y, edge_x, edge_y, imagefilepath_r)
        radiusInfo.to_excel(path + 'radiusInfo_' + f.split(' ')[0] + '.xlsx')
        t = t + 1
        print("幅宽[{}]画图完成 ".format(f.split(' ')[0]))
        del radiusInfo
        del data
    files_data.to_excel('D:\mmm\轨迹数据集\\test7\widthInfo_test7.xlsx')


def test8():
    """
    用回归方程计算的最优半径检测边界，验证回归方程的正确
    :return:
    """

    file_index_data_path = r'D:\mmm\轨迹数据集\test8\test8-file-index.xls'
    file_index_data = pda.read_excel(file_index_data_path)

    path = 'D:\mmm\轨迹数据集\汇总\\'
    imagefilepath = r'D:\mmm\轨迹数据集\test8\image\\'
    for i, f, r in zip(file_index_data.loc[:, '序号'], file_index_data.loc[:, '文件名称'], file_index_data.loc[:, '最优半径']):
        data = GetData(path + f)
        # 边界检测
        start = time.time()
        edge_x, edge_y, edge_index = alpha_shape_2D(data, r)
        end = time.time()
        # 面积计算
        area, times = calFiledArea([edge_x, edge_y])  # 根据检测出的边界点计算面积

        # 登记
        file_index_data.loc[i, 'edgeNum'] = len(edge_x)
        file_index_data.loc[i, '边界点检测耗时'] = round(end - start, 2)
        file_index_data.loc[i, '地块面积'] = area

        # 绘图
        imagefilepath_r = imagefilepath + str(i) + '_' + f.split(' ')[0] + '_R=' + str(round(r, 2)) + '.png'
        plotEdge(data.x, data.y, edge_x, edge_y, imagefilepath_r)
        del data

    file_index_data.set_index('序号', inplace=True)
    file_index_data.to_excel(file_index_data_path)


def test9():
    """
    重新探索 1.4 幅宽的最优半径

    :return:
    """
    files_data = pda.read_excel('D:\\mmm\\轨迹数据集\\test9\\test9_edgeInfo_1-4.xlsx')
    path = 'D:\mmm\轨迹数据集\\test9\\'

    t = 0
    for f in files_data.文件名:
        a = 0.2
        radius = np.round(np.arange(a, 10.1, 0.2), 2)  # 设置半径的选项值
        imagepath = path + str(t) + '_num_' + f.split(' ')[0]
        if not os.path.exists(imagepath):
            os.makedirs(imagepath)
            print("[{}]创建成功 ".format(imagepath))

        data = GetData('D:\mmm\轨迹数据集\汇总\\' + f)

        # 边界图片命名
        imagefile = f.split(' ')
        imagefile[1] = '-image.png'
        imagefile = ''.join(imagefile)
        imagefilepath = imagepath + '\\' + imagefile
        # print(imagefilepath)
        radiusInfo = pda.DataFrame(
            columns=['radius', 'pointNum', 'edgeNum', '边界点检测耗时(s)', '地块面积（平方米）'])

        i = 0
        for r in radius:
            imagefilepath_r = imagefilepath
            # 边界检测
            start = time.time()
            edge_x, edge_y, edge_index = alpha_shape_2D(data, r)
            end = time.time()
            # 面积计算
            area, times = calFiledArea([edge_x, edge_y])  # 根据检测出的边界点计算面积
            # 登记
            radiusInfo.loc[i] = [r, data.shape[0], len(edge_x), round(end - start, 2), area]
            i += 1
            imagefilepath_r = imagefilepath_r.replace('.', '-' + str(r) + '.')
            plotEdge(data.x, data.y, edge_x, edge_y, imagefilepath_r)
        radiusInfo.to_excel(path + str(t) + '_radiusInfo_' + f.split(' ')[0] + '.xlsx')
        t = t + 1
        print("幅宽[{}]画图完成 ".format(f.split(' ')[0]))
        del radiusInfo
        del data
    files_data.to_excel('D:\mmm\轨迹数据集\\test9\widthInfo_test9.xlsx')


def getBestRadius(filedata):
    """
    :param filedata: 地块轨迹文件
    :return: 最优半径
    """
    # 计算时间间隔
    filepointCount = filedata.shape[0]
    for i in range(1, filepointCount):

        if type(filedata.loc[i, 'GPS时间']) == str:
            startTime = pda.Timestamp(filedata.loc[i - 1, 'GPS时间'])
            endTime = pda.Timestamp(filedata.loc[i, 'GPS时间'])
        else:
            startTime = filedata.loc[i - 1, 'GPS时间']
            endTime = filedata.loc[i, 'GPS时间']
        filedata.loc[i, '时间间隔'] = (endTime - startTime).seconds

    yangTime = filedata.时间间隔.mode()[0]

    # 计算平均速度
    filedata.rename(columns={'速度(km/h)': 'speed'}, inplace=True)
    workPoint = filedata[filedata.工作状态 == True]
    speedMean = workPoint.speed.sum() / workPoint.shape[0]  # 根据工作状态中的点速度求平均速度 km/h
    speedMean = speedMean * 0.2777778  # m/s

    # 获取作业幅宽
    width = filedata.loc[:, '幅宽(m)'].mode()[0]

    # test10 ,12
    r = -6.909 + 0.207 * width + 6.487 * speedMean + 3.855 * yangTime - 1.742 * yangTime * speedMean + 2.336 * 0.00001 * filepointCount

    # 用幅宽 和 点间距 与 半径的回归方程 test11
    # r = 0.905 + 0.721 * width + 0.273 * yangTime * speedMean

    return r


def test10():
    """
    用带轨迹点的回归方差预测最优半径，并进行全量边界检测及面积计算
    :return:
    """
    testpath = r'D:\mmm\轨迹数据集\test10'
    filedpath = 'D:\mmm\轨迹数据集\汇总\\'
    imagefilepath = testpath + '/image/'
    edge_path = testpath + '/edgePoint/'

    file_index_data = pda.read_excel(r'D:\mmm\轨迹数据集\test10\test10_轨迹索引-v1.0.xlsx')
    # result_info = pda.DataFrame(columns=['文件序号', 'edgeNum', '边界点检测耗时', '地块面积','最优半径'])
    result_info = pda.read_excel(r'D:\mmm\轨迹数据集\test10\test10_result_info.xlsx')
    file_index_data.dropna()
    start_0 = time.time()
    print("程序开始 {}".format(start_0))
    for i, f in zip(file_index_data.loc[934:1071, '新文件序号'], file_index_data.loc[934:1071, '文件名称']):
        if type(f) != str:
            continue
        data = GetData(filedpath + f)

        iStr = '{:0>5.0f}'.format(i)
        # 根据回归方程预测最优半径
        r = getBestRadius(data)
        print('{}的最优半径为：[{}]'.format(iStr, r))

        # 边界检测
        start = time.time()
        edge_x, edge_y, edge_index = alpha_shape_2D(data, r)
        end = time.time()
        print('\t边界检测 完成')

        # 面积计算
        area, times = calFiledArea([edge_x, edge_y])  # 根据检测出的边界点计算面积
        print('\t面积计算 完成')

        # 保存边界点
        edge_excel_name = iStr + '_edgePoint_R=' + str(round(r, 2)) + '.xlsx'
        edge_data = pda.DataFrame({'x': edge_x, 'y': edge_y})
        edge_data.to_excel(edge_path + edge_excel_name)
        print('\t边界点保存 完成')

        # 绘制边界图
        imagefilepath_r = imagefilepath + iStr + '_' + 'edgeImage_R=' + str(round(r, 2)) + '.png'
        plotEdge(data.x, data.y, edge_x, edge_y, imagefilepath_r)
        print('\t边界绘制 完成')

        # 登记
        result_info.loc[int(i), '文件序号'] = iStr
        result_info.loc[int(i), 'edgeNum'] = len(edge_x)
        result_info.loc[int(i), '边界点检测耗时'] = round(end - start, 2)
        result_info.loc[int(i), '地块面积'] = area
        result_info.loc[int(i), '最优半径'] = r

        print('\t登记 完成')
        del data
        del edge_data

        print('\t{}处理完毕'.format(iStr))

        if i % 10 == 0:  # 每登记10个保存一次
            result_info.to_excel(testpath + '/test10_result_info.xlsx')
            print(time.time())

    # result_info.set_index('序号', inplace=True)
    result_info.to_excel(testpath + '/test10_result_info.xlsx')
    end_0 = time.time()
    print("程序结束 {}".format(end_0 - start_0))


def test11():
    """
    用带轨迹点的回归方差预测最优半径，并进行全量边界检测及面积计算
    :return:
    """
    testpath = r'D:\mmm\轨迹数据集\test11'
    filedpath = 'D:\mmm\轨迹数据集\汇总\\'
    imagefilepath = testpath + '/image/'
    edge_path = testpath + '/edgePoint/'

    file_index_data = pda.read_excel(r'D:\mmm\轨迹数据集\test11\test11_轨迹索引-v1.0.xlsx')
    # result_info = pda.DataFrame(columns=['文件序号', 'edgeNum', '边界点检测耗时', '地块面积','最优半径'])
    result_info = pda.read_excel(r'D:\mmm\轨迹数据集\test11\test11_result_info.xlsx')
    file_index_data.dropna()
    start_0 = time.time()
    print("程序开始 {}".format(start_0))
    for i, f in zip(file_index_data.loc[541:933, '新文件序号'], file_index_data.loc[541:933, '文件名称']):
        if type(f) != str:
            continue
        data = GetData(filedpath + f)

        iStr = '{:0>5.0f}'.format(i)
        # 根据回归方程预测最优半径
        r = getBestRadius(data)
        print('{}的最优半径为：[{}]'.format(iStr, r))

        # 边界检测
        start = time.time()
        edge_x, edge_y, edge_index = alpha_shape_2D(data, r)
        end = time.time()
        print('\t边界检测 完成')

        # 面积计算
        area, times = calFiledArea([edge_x, edge_y])  # 根据检测出的边界点计算面积
        print('\t面积计算 完成')

        # 保存边界点
        edge_excel_name = iStr + '_edgePoint_R=' + str(round(r, 2)) + '.xlsx'
        edge_data = pda.DataFrame({'x': edge_x, 'y': edge_y})
        edge_data.to_excel(edge_path + edge_excel_name)
        print('\t边界点保存 完成')

        # 绘制边界图
        imagefilepath_r = imagefilepath + iStr + '_' + 'edgeImage_R=' + str(round(r, 2)) + '.png'
        plotEdge(data.x, data.y, edge_x, edge_y, imagefilepath_r)
        print('\t边界绘制 完成')

        # 登记
        result_info.loc[int(i), '文件序号'] = iStr
        result_info.loc[int(i), 'edgeNum'] = len(edge_x)
        result_info.loc[int(i), '边界点检测耗时'] = round(end - start, 2)
        result_info.loc[int(i), '地块面积'] = area
        result_info.loc[int(i), '最优半径'] = r

        print('\t登记 完成')
        del data
        del edge_data

        print('\t{}处理完毕'.format(iStr))

        if i % 10 == 0:  # 每登记10个保存一次
            result_info.to_excel(testpath + '/result_info.xlsx')
            print(time.time())

    # result_info.set_index('序号', inplace=True)
    result_info.to_excel(testpath + '/test11_result_info.xlsx')
    end_0 = time.time()
    print("程序结束 {}".format(end_0 - start_0))


def test12():
    """
    用带轨迹点的回归方差预测最优半径，并进行全量边界检测及面积计算
    :return:
    """
    testpath = r'D:\mmm\轨迹数据集\test12'
    filedpath = 'D:\mmm\轨迹数据集\汇总\\'
    imagefilepath = testpath + '/imageNOT/'
    edge_path = testpath + '/edgePoint/'

    file_index_data = pda.read_excel(r'D:\mmm\轨迹数据集\test12\test12_轨迹索引-v1.0.xlsx')
    # result_info = pda.DataFrame(columns=['文件序号', 'edgeNum', '边界点检测耗时', '地块面积', '最优半径', '图片链接'])
    result_info=pda.read_excel(r'D:\mmm\轨迹数据集\test12\test12_result_info.xlsx')
    result_info.set_index('文件序号',drop=True,inplace=True)
    file_index_data.dropna()
    start_0 = time.time()
    edgeIndex = 0

    edgeFileList = os.listdir(r'D:\mmm\轨迹数据集\test12\edgePoint')

    print("程序开始 {}".format(start_0))
    for i, f in zip(file_index_data.loc[:, '新文件序号'], file_index_data.loc[:, '文件名称']):
        if type(f) != str:
            continue


        iStr = '{:0>5.0f}'.format(i)

        edgeF=edgeFileList[edgeIndex]
        edgeIndex = edgeIndex +1
        edge=pda.read_excel(testpath+'/edgePoint/'+edgeF)
        result_info.loc[int(i), 'edgepointfile'] = edgeF

        if not result_info.loc[int(i), 'flag']:
            data = GetData(filedpath + f)
            #
            temp=edgeF.split('=')[1]
            r = temp[0:-5]

            # 绘制边界图
            imagefilepath_r1 = imagefilepath + iStr + '_' + 'edgeImage_R=' + r + '.jpg'
            # imagefilepath_r2 = testpath + '/justWorkImage/' + iStr + '_' + 'workTrajectoryImage' + '.jpg'
            # imagefilepath_r3 = testpath + '/allPointImage/' + iStr + '_' + 'moveTrajectoryImage' + '.jpg'
            # imagefilepath_r4 = testpath + '/equalImage/' + iStr + '_' + 'moveTrajectoryImage' + '.jpg'

            # plotEdge(data.x, data.y, edge_x, edge_y) # 只绘制，不保存
            # plotEdgefor12(data, edge.x, edge.y)


            plotEdgefor12(data, edge.x, edge.y, imagefilepath_r1)
            # plotEdgefor12(data, edge.x, edge.y, imagefilepath_r2)
            # plotEdgefor12(data, edge.x, edge.y, imagefilepath_r3)
            # plotEdgefor12(data, edge.x, edge.y, imagefilepath_r4)
            # print('\t边界绘制 完成')
            # result_info.loc[int(i), '边界图片链接'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r1, iStr + '_edge')
            # result_info.loc[int(i), '工作轨迹图片链接'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r2, iStr + '_work')
            # result_info.loc[int(i), '运动轨迹图片链接'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r3, iStr + '_move')
            # result_info.loc[int(i), '运动轨迹图片链接(真)'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r4, iStr + '_equal')


            # print('\t登记 完成')
            # del data
        del edge

        print('\t{}处理完毕'.format(iStr))

        # if i % 10 == 0:  # 每登记10个保存一次
        #     result_info.to_excel(testpath + '/test12_result_info.xlsx')
        #     print(time.time())

    # result_info.set_index('序号', inplace=True)
    # result_info.to_excel(testpath + '/test12_result_info.xlsx')
    end_0 = time.time()
    print("程序结束 {}".format(end_0 - start_0))


def plotEdgefor12(data,  edge_x, edge_y, path=''):
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

    plt.figure(figsize=(19.2, 9.36), dpi=100)


    if 'justWorkImage' in path:
        work = data[data['工作状态'] == True]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签

        plt.title(path.split('/')[-1])
        plt.plot(work.x, work.y, '-', color='k',linewidth=1)

    elif 'allPointImage' in path:
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.title(path.split('/')[-1])
        plt.plot(data.x, data.y, '-', color='k', linewidth=1)

    elif 'equal' in path:
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.title(path.split('/')[-1])
        plt.plot(data.x, data.y, '-', color='k', linewidth=1)
        plt.axis('equal')  # 通过更改轴限制设置相等的缩放比例（即，使圆成为圆形）

    else:
        noWork = data[data['工作状态'] == False]
        work = data[data['工作状态'] == True]
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.title(path.split('/')[-1])
        plt.plot(data.x, data.y, '-', color='green', linewidth=1)
        plt.plot(noWork.x, noWork.y, 'bo', color='k', linewidth=1, markersize=2)
        plt.plot(work.x, work.y, 'bo', color='pink', linewidth=1, markersize=2)
        plt.plot(edge_x, edge_y, '*-', color='r', markersize=6)
        plt.legend(('农机运动轨迹线', '非工作轨迹点', '工作轨迹点', '边界线'),loc='best')
        # plt.axis('equal')  # 通过更改轴限制设置相等的缩放比例（即，使圆成为圆形）

    plt.axis('off')
    if path:
        plt.savefig(path,format='jpg',dpi=500)
    else:
        plt.show()
    plt.close()




def allFilesGetEdgeWithSameWidth():
    # 选好最优半径后对同一幅宽的的全量文件进行边界检测
    files_data = filesWithDifferentWidth('D:\mmm\轨迹数据集\轨迹索引-v1.0.xlsx')
    path = 'D:\mmm\轨迹数据集'
    # radata=pda.read_excel(r'D:\mmm\轨迹数据集\image-居中轨迹点文件\widthInfo.xlsx')

    w = files_data.loc[1, '幅宽']
    imagepath = path + '\\image'
    if not os.path.exists(imagepath):
        os.makedirs(imagepath)
        print("[{}]创建成功 ".format(imagepath))
    count = files_data[files_data.幅宽 == w].shape[0]
    edgeInfo = pda.DataFrame(columns=['文件名', 'pointNum', 'edgeNum', '边界点检测耗时(s)', '地块面积（平方米）', '面积计算耗时(s)'])
    t = 0
    r = 3.6  # 幅宽1.4的最优半径
    for f in files_data.loc[0:count - 1, '文件名称']:
        # a = 2
        # radius = np.round(np.arange(a, 10.1, 0.2), 2)  # 设置半径的选项值
        # imagepath=imagepath1+'_num_' + str(t)

        if '476' in f:
            continue
        imagefile = f.split(' ')
        imagefile[1] = '-image.png'
        imagefile = ''.join(imagefile)
        imagefilepath = imagepath + '\\' + imagefile
        # print(imagefilepath)

        data = GetData('D:\mmm\轨迹数据集\汇总\\' + f)

        i = 0

        # for r in radius:
        imagefilepath_r = imagefilepath
        start = time.time()
        edge_x, edge_y, edge_index = alpha_shape_2D(data, r)
        end = time.time()

        area, times = calFiledArea([edge_x, edge_y])  # 根据检测出的边界点计算面积
        edgeInfo.loc[t] = [f, data.shape[0], len(edge_x), round(end - start, 2), area, times]
        # i += 1
        imagefilepath_r = imagefilepath_r.replace('.', '-' + str(r) + '.')
        plotEdge(data.x, data.y, edge_x, edge_y, imagefilepath_r)

        # radiusInfo.to_excel(path + '/image/radiusInfo_' + str(t) + '.xlsx')
        t = t + 1
        # print("幅宽[{}]画图完成 ".format(w))
        # del edgeInfo
        del data
    edgeInfo.to_excel(path + '/image/edgeInfo' + str(w).replace('.', '-') + '.xlsx')
    files_data.to_excel('D:\mmm\轨迹数据集\\image\widthInfo.xlsx')


def calFiledArea(edge):
    """
    根据边界点 利用多边形计算公式 计算地块面积
    :param edge: 地块边界点(默认是dataframe格式)
    :return: 地块面积，以及面积计算时长
    """
    if type(edge) != pda.pandas.core.frame.DataFrame:
        t = pda.DataFrame(columns=['x', 'y'])
        t.x = edge[0]
        t.y = edge[1]
        edge = t

    count = edge.shape[0] - 1  # 获取边界点个数
    i = 0
    temp = 0
    area = 0
    # 多边形面积计算
    start = time.time()
    while i < count:
        temp += edge.x[i] * edge.y[i + 1] - edge.x[i + 1] * edge.y[i]
        i += 1
    area = 0.5 * ma.fabs(temp)  # 平方米  （多边形顶点按逆时针排列则是正值，顺时针排列则是负值）
    end = time.time()
    times = round(end - start, 2)
    # print(times)

    return area, times


def findRadius():
    """
    搜寻合适的圆半径 alpha
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
    color_type = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16',
                  'C17', 'C18', 'C19', 'C20']
    t = np.random.randint(0, 20)
    cir1 = Circle(xy=(cicle_x, cicle_y), radius=radius, alpha=0.5, edgecolor=color_type[t], facecolor='None',
                  lw=1)  # 第一个参数为圆心坐标，第二个为半径 #第三个为透明度（0-1）
    ax.add_patch(cir1)
    # plt.axis('scaled') #通过更改绘图框的尺寸设置相等的缩放比例（即，使圆成为圆形）
    plt.axis('equal')  # 通过更改轴限制设置相等的缩放比例（即，使圆成为圆形）
    plt.axis('off')


def calSpeedMean(path):
    edgeInfoData = pda.read_excel(path)
    datapath = r'D:\mmm\轨迹数据集\汇总'
    t = 0
    for f in edgeInfoData.loc[:, '文件名']:  # 获取文件名称
        filepath = datapath + '/' + f
        filedata = pda.read_excel(filepath)  # 读取轨迹文件
        filedata.rename(columns={'速度(km/h)': 'speed'}, inplace=True)
        workPoint = filedata[filedata.工作状态 == True]
        speedMean = workPoint.speed.sum() / workPoint.shape[0]  # 根据工作状态中的点速度求平均速度
        # fIndex = edgeInfoData[edgeInfoData.文件名==f].index
        edgeInfoData.loc[t, '平均速度'] = speedMean  # 登记平均速度

        # 计算时间间隔
        filepointCount = filedata.shape[0]
        for i in range(1, filepointCount):

            if type(filedata.loc[i, 'GPS时间']) == str:
                startTime = pda.Timestamp(filedata.loc[i - 1, 'GPS时间'])
                endTime = pda.Timestamp(filedata.loc[i, 'GPS时间'])
            else:
                startTime = filedata.loc[i - 1, 'GPS时间']
                endTime = filedata.loc[i, 'GPS时间']
            filedata.loc[i, '时间间隔'] = (endTime - startTime).seconds

        # edgeInfoData.loc[t,'采样间隔时间'] = filedata.时间间隔.mode()
        edgeInfoData.loc[t, '采样间隔时间'] = filedata.时间间隔.mode()[0]
        print(t)

        # print(filedata.时间间隔.mode())
        # print(fIndex)
        # print(edgeInfoData.loc[t, '采样间隔时间'])
        t = t + 1
        # if '449' in f:
        #     print(f)
        # print(f)
        del filedata

    edgeInfoData.set_index('index', inplace=True)
    edgeInfoData.to_excel(path)


def calWorkTime():
    """
    计算一块地的总作业时间
    :param data: 地块作业轨迹点
    :return: 作业总时间
    """
    fn = askopenfilenames(title='选择文件', filetypes=[('*', 'csv'), ('*', 'xls'), ('*', 'xlsx')])
    if fn:
        info = pda.DataFrame(columns=['filename', 'width'])
        for f in fn:
            # data = GetData(r'D:\mmm\轨迹数据集\汇总\00002 耕-大-梭==黑02-S45274_2017-9-21==0921-0313-filed.xls')
            if (f.split('.')[1] == 'csv'):
                data = pda.read_csv(f)
            else:
                data = pda.read_excel(f)
            count = data.shape[0]
            flag = 0  # 标识开始结束时间
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
# calWorkTime()

# data = GetData(r'D:\Downloads\湘12-E1136_2016-10-13==1013-0746-field.csv')
# data.to_excel(r'D:\Downloads\湘12-E1136_2016-10-13==1013-0746-field-2.xlsx')
# data = filesWithDifferentWidth('D:\mmm\轨迹数据集\轨迹索引-v1.0.xlsx')
# data.to_excel(r'D:\mmm\轨迹数据集\widthinfo-20210303.xlsx')
#
# findRadiusFromDifferentWidth()
# findRadiusFromSameWidth()
# allFilesGetEdgeWithSameWidth()
# justShowEdge(r'D:\mmm\轨迹数据集\汇总\00142 耕-小-套==鲁16_543101_2020-11-6==1106-0200-filed.xlsx', 5.02)
# calSpeedMean('D:\\mmm\\轨迹数据集\\image\\edgeInfo1-4.xlsx')

# test7()
# test8()
# test9()
# test10()
# test11()
test12()
#
#
# R=getBestRadius(GetData(r'D:\mmm\轨迹数据集\汇总\00530 耕-中-梭==新42_901117_2018-9-19==0919-1306-filed.xlsx'))
# print(R)
