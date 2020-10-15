# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 17:52:56 2020

@author: Administrator
"""

import numpy as npy
import re
import math as ma
import pandas as pda
import matplotlib.pyplot as plt
import tkinter.messagebox
from tkinter.filedialog import *
import time
import os

#  自己的模块
from SplitFileByMoreAttributes_20200925_v3_0 import SplitfieldByMoreAtrributes


class GetPoint:

    def __init__(self, longtitude, latitude):
        self.latitude = latitude  # 纬度
        self.longtitude = longtitude  # 经度

    def ToY(self, weidu):
        a = 6378137  # 赤道圆的平均半径为 6378137 m
        b = 6356752  # 在WGS-84 中半短轴的长度为 6356752 m
        a1 = ma.pow(a, 2)
        b1 = ma.pow(b, 2)
        BO1 = ma.pow(ma.tan(self.latitude), 2)
        BO2 = ma.pow(1 / ma.tan(self.latitude), 2)
        Xo = a1 / ma.sqrt(b1 * BO1 + a1)  # 参考点的横坐标
        Yo = b1 / ma.sqrt(a1 * BO2 + b1)  # 参考点的纵坐标

        AO1 = ma.pow(ma.tan(weidu), 2)
        AO2 = ma.pow(1 / ma.tan(weidu), 2)
        Xa = a1 / ma.sqrt(b1 * AO1 + a1)  # 目标点的横坐标
        Ya = b1 / ma.sqrt(a1 * AO2 + b1)  # 目标点的纵坐标
        Y = ma.sqrt(ma.pow(Xa - Xo, 2) + ma.pow(Ya - Yo, 2))  # 目标点与参考点在平面坐标系中纵轴方向的距离
        if weidu < self.latitude:
            Y = -Y
        return Y

    def ToX(self, jingdu):
        a = 6378137
        b = 6356752

        a1 = ma.pow(a, 2)
        b1 = ma.pow(b, 2)
        BO1 = ma.pow(ma.tan(self.latitude), 2)
        Xo = a1 / ma.sqrt(b1 * BO1 + a1)
        X = Xo * ma.fabs(jingdu - self.longtitude)  # 目标点与参考点之间在平面坐标系中横轴方向上的距离
        if jingdu < self.longtitude:
            X = -X
        return X



def slipt_by_toolState(data):
    line = len(data.values)  # 获取数据有多少行
    a = list(data['作业深度(mm)'])
    b = list(data['机具状态'])
    c = list(data['经度'])  # 经度
    d = list(data['纬度'])  # 纬度
    e = c[0]  # 第一个经度
    f = d[0]  # 第一个纬度

    g = GetPoint(e, f)  # 获得参照点

    h = []  # 由纬度转换后的Y轴坐标值
    for i in range(len(c)):
        h.append(g.ToY(c[i]))
    k = []  # 由经度转换后的X轴坐标值
    for j in range(len(d)):
        k.append(g.ToX(d[j]))

    for i in range(line):
        # 根据机具状态和作业深度进行分割，空行轨迹点视为无效点不进行转换
        if a[i] == 0 and b[i] == 0:
            h[i] = 0
            k[i] = 0
    h.append(0)
    k.append(0)
    return h, k


def openfile():
    r = askopenfilenames(title='打开文件', filetypes=[('All File', '*')])
    if r != '':

        for num in range(len(r)):
            try:
                if re.match("(.)*.csv$", r[num]) is not None:
                    data = pda.read_csv(r[num])  # 直接对文件路径名及文件进行read 不需要提前打开
                else:
                    data = pda.read_excel(r[num])

            except Exception as e:
                print(tkinter.messagebox.showerror("打开文件出错", "第" + str(num + 1) + "张表格报错" + " " + repr(e) + os.linesep))
                break

            try:

                # h, k 是转换成平面坐标后的经纬度
                # h, k = slipt_by_toolState(data)
                # h, k = slipt_by_headingAngle(data)

                data, h, k, shape_x, shape_y = SplitfieldByMoreAtrributes(data, r[num])
                m = []
                n = []

                p = 1  # 用于图片命名，与地块标志相对应
                count = 1  # 用于计算图片数量
                fileName = r[num]
                fileName = fileName.split('.')
                # fileName = fileName[0] + '-tupian/'
                # os.mkdir(fileName)



                indexOfA = [i for i, x in enumerate(h) if x == 'a']
                # indexOfShapeA = [i for i, x in enumerate(shape_x) if x == 'a']
                i = 0
                while i < len(indexOfA):
                    if i == 0 and indexOfA[i] > 20:
                        m = h[0:indexOfA[i]]
                        n = k[0:indexOfA[i]]
                        # sh_x = shape_x[0:indexOfShapeA[i]]
                        # sh_y = shape_y[0:indexOfShapeA[i]]
                    elif i != 0 and indexOfA[i] - indexOfA[i - 1] - 1 > 20:
                        m = h[indexOfA[i - 1] + 1:indexOfA[i]]
                        n = k[indexOfA[i - 1] + 1:indexOfA[i]]
                        # sh_x = shape_x[indexOfShapeA[i - 1] + 1:indexOfShapeA[i]]
                        # sh_y = shape_y[indexOfShapeA[i - 1] + 1:indexOfShapeA[i]]
                    else:
                        i += 1
                        p += 1
                        continue
                    plt.plot(m, n, color='k', linewidth=1)
                    # plt.plot(sh_x, sh_y, color='r', linewidth=2)
                    plt.axis('off')
                    plt.savefig(fileName[0] + '-{}.jpg'.format(p))
                    plt.close()
                    label1.config(text="生成了%d张图片" % count)
                    p += 1
                    count += 1
                    i += 1
                    # del m, n, sh_x, sh_y

            except Exception as e:
                print(tkinter.messagebox.showerror("Error", "第" + str(num + 1) + "张表格报错" + " " + repr(e) + os.linesep))
            '''g = open('mistake.txt','a+')
            g.write("第"+str(num+1)+"张表格报错"+" "+repr(e)+os.linesep)
            g.close()'''
            continue
            del data


'''
        list_dirs = os.listdir("G:/tupian")
        for d in range(len(list_dirs)):
            try:
                fp = open("G:/tupian/%s" % list_dirs[d], 'rb')
                img = fp.read()
            except IOError:
                continue
            finally:
                fp.close()
            # 创建连接
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='shiyan',
                                   charset='utf8')
            # 创建游标
            cursor = conn.cursor()
            # 注意使用Binary()函数来指定存储的是二进制
            sql = "INSERT INTO images (image) VALUES  (%s)"
            try:
                cursor.execute(sql, img)
                # 提交，不然无法保存新建或者修改的数据
                conn.commit()
            except Exception as e:
                conn.rollback()
                g = open('mistake.txt', 'a+')
                g.write("导入第" + str(num + 1) + "条数据报错" + " " + repr(e) + os.linesep)
                g.close()
            finally:
                # 关闭游标
                cursor.close()
                # 关闭连接
                conn.close()

            label2.config(text="导入了%d张图片" % (d + 1))
'''
root = Tk()
root.title('批处理文件')
root.geometry("400x200")
label1 = Label(root, text='生成图片数', height=1, width=20, fg="black")
label1.pack(pady=10)
label2 = Label(root, text='导入数据库图片数', height=1, width=20, fg="black")
label2.pack()
btn1 = Button(root, text='选择导入的文件', command=openfile)
btn1.pack(pady=10)

root.mainloop()
