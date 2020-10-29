from scipy.spatial import Delaunay
import numpy as np
from collections import defaultdict
import pandas as pda
import math as ma
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
import time


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
    :param a: a点坐标
    :param b: b点坐标
    :return: dis 直线距离
    """
    p1 = np.array(a)
    p2 = np.array(b)

    dis = ma.sqrt(sum(np.power(p2 - p1, 2)))
    return dis


def alpha_shape_2D(data, radius):
    """
    alpha shapes 算法检测边缘
    :param x: 原始点坐标集 x轴
    :param y: 原始点坐标集 y轴
    :param radius: 圆半径
    :return: 边缘点集
    """

    x = data.x
    y = data.y
    count = len(x)
    i = 0
    temp_i = i
    edge_x = []
    edge_y = []
    edge=[]
    edge_len = 0

    while (i < count):
        i_range = np.array([t for t, v in enumerate(x < x[i] + radius) if v == True])
        i_range = i_range[[t for t, v in enumerate(data.loc[i_range, 'x'] > x[i] - radius) if v == True]]
        i_range = i_range[[t for t, v in enumerate(data.loc[i_range, 'y'] < y[i] + radius) if v == True]]
        i_range = i_range[[t for t, v in enumerate(data.loc[i_range, 'y'] > y[i] - radius) if v == True]]
        # print(i)
        # tes = i_range > i
        # rope = []
        # for t in range(len(i_range)):
        #     if tes[t] == True:
        #         rope.append(t)
        # i_range =i_range[rope]

        if i==590:
            print(i)

        for k in i_range:
            # if k <= temp_i:
            #     continue

            if edge_x.count(x[k])>0:
                continue

            dis = distance((x[i], y[i]), (x[k], y[k]))
            if dis > 2 * radius or dis < 0.5:
                continue



            # 线段中点
            center_x = (x[k] + x[i]) * 0.5
            center_y = (y[k] + y[i]) * 0.5

            # 方向向量
            direct_x = x[k] - x[i]
            direct_y = y[k] - y[i]

            if direct_x == 0 and direct_y == 0:
                continue

            # 法向量 及其单位化

            nomal_x = -direct_y / ma.sqrt(pow(direct_x, 2) + pow(direct_y, 2))
            nomal_y = direct_x / ma.sqrt(pow(direct_x, 2) + pow(direct_y, 2))

            # 圆心到直线距离
            disOfcenter = ma.sqrt(pow(radius, 2) - 0.25 * pow(dis, 2))

            if nomal_x != 0:
                a = ma.sqrt(pow(disOfcenter, 2) / (1 + pow(nomal_y / nomal_x, 2)))
                b = a * (nomal_y / nomal_x)
            else:
                a = 0
                b = radius

            cicle1_x = center_x + a
            cicle1_y = center_y + b

            cicle2_x = center_x - a
            cicle2_y = center_y - b

            # cicle1_x = center_x + disOfcenter * nomal_x
            # cicle1_y = center_y + disOfcenter * nomal_y
            #
            # cicle2_x = center_x - disOfcenter * nomal_x
            # cicle2_y = center_y - disOfcenter * nomal_y

            # 检测圆内是否有其他点
            b1 = False
            b2 = False

            inSquare = np.array([t for t, v in enumerate(x < cicle1_x + radius) if v == True])
            inSquare = inSquare[[t for t, v in enumerate(data.loc[inSquare, 'x'] > cicle1_x - radius) if v == True]]
            inSquare = inSquare[[t for t, v in enumerate(data.loc[inSquare, 'y'] < cicle1_y + radius) if v == True]]
            inSquare = inSquare[[t for t, v in enumerate(data.loc[inSquare, 'y'] > cicle1_y - radius) if v == True]]
            if len(inSquare) != 0:
                for j in inSquare:
                    if j == i or j == k:
                        continue
                    else:
                        d = distance((x[j], y[j]), (cicle1_x, cicle1_y))
                        if d <= radius:  # 圆内有点 ，跳过
                            b1 = True
                            break
            inSquare = np.array([t for t, v in enumerate(x < cicle2_x + radius) if v == True])
            inSquare = inSquare[[t for t, v in enumerate(data.loc[inSquare, 'x'] > cicle2_x - radius) if v == True]]
            inSquare = inSquare[[t for t, v in enumerate(data.loc[inSquare, 'y'] < cicle2_y + radius) if v == True]]
            inSquare = inSquare[[t for t, v in enumerate(data.loc[inSquare, 'y'] > cicle2_y - radius) if v == True]]
            if len(inSquare) != 0:
                for j in inSquare: # 与原两个点的坐标点一样
                    if j == i or j == k or distance((x[j], y[j]), (x[i], y[i]))==0 :
                        continue
                    else:
                        d = distance((x[j], y[j]), (cicle2_x, cicle2_y))
                        if d <= radius:  # 圆内有点 ，跳过
                            b2 = True
                            break


            if b1 == False or b2 == False:
                if edge_x.count(x[i])<1:
                    edge_x.append(x[i])
                    edge_y.append(y[i])
                    edge.append(i)
                if edge_x.count(x[k]) < 1:
                    edge_x.append(x[k])
                    edge_y.append(y[k])
                    edge.append(k)
                temp_k = k
                # print('k={}'.format(k))


        # print("edge_len={},i={}".format(edge_len,i))
        print(i)
        if edge_len < len(edge_x)  :
            temp_i=i
            i=temp_k
            edge_len = len(edge_x)
        else:
            temp_i = i
            i = i + 1

        # i = i + 1

    dd = pda.DataFrame({'point':edge,'x':edge_x,'y':edge_y})
    dd.to_excel('D:/mmm/python/轨迹测试数据/0927-将文件进行分割成多个文件/112.xlsx')
    return edge_x, edge_y


def GetData():
    """
    读取表格数据
    读取表格数据
    :return:
    """
    data = pda.read_excel(
        # 'D:/mmm/python/轨迹测试数据/0927-将文件进行分割成多个文件/新31-Y3616_2016-10-24-section/新31-Y3616_2016-10-24==1023-2204-filed.xlsx')
        # 'D:/mmm/python/轨迹测试数据/0927-将文件进行分割成多个文件/新42-98765_2016-11-10-section/新42-98765_2016-11-10==1109-2229-field.xlsx')
        'D:/mmm/python/轨迹测试数据/0927-将文件进行分割成多个文件/新42-98765_2016-11-10-section/新42-98765_2016-11-10==1110-1329-field.xlsx')
    # data = pda.read_excel(
    #     'D:/mmm/python/轨迹测试数据/0928-分析数据特征/新40-60002-修-2墨卡托坐标-section/新40-60002-修-2墨卡托坐标==0420-1634-filed.xlsx')

    # data = pda.read_excel(
    #     'D:/mmm/python/轨迹测试数据/0928-分析数据特征/新31-Y3616_2016-10-24.xlsx')

    return data


data = GetData()

start = time.time()
edge_x, edge_y = alpha_shape_2D(data, 8)
end = time.time()
print('运行时间：{}'.format(end-start))

" 这一段是标记每个点的坐标"
# i=0
# while i <len(data.x):
#     plt.text(data.x[i],data.y[i],i,ha='center',va='bottom',fontsize=8,color='b')
#     i+=1
"结束"

i=0
while i <len(edge_x):
    plt.text(edge_x[i],edge_y[i],i,ha='center',va='bottom',fontsize=11,color='b')
    i+=1

plt.plot(data.x, data.y, 'bo-',color='k',linewidth=1,markersize=2)
plt.plot(edge_x, edge_y, '*-',color='r',markersize=6)

plt.axis('off')
plt.show()
