# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 17:52:56 2020

@author: Administrator
"""

import numpy as npy
# import pymysql
import re
import math as ma
import pandas as pda
import matplotlib.pyplot as plt
import tkinter.messagebox
from tkinter.filedialog import *


class GetPoint:

    def __init__(self, latitude, longtitude): # 初始化 输入参考起点经纬度 为参考坐标的 圆心
        self.latitude = latitude  # 经度
        self.longtitude = longtitude  # 纬度

    def ToY(self, weidu, weidu1):
        a = 6378137  # 赤道圆的平均半径为 6378137 m
        b = 6356752  # 在WGS-84 中半短轴的长度为 6356752 m
        a1 = ma.pow(a, 2)
        b1 = ma.pow(b, 2)
        BO1 = ma.pow(ma.tan(weidu), 2)
        BO2 = ma.pow(1 / ma.tan(weidu), 2)
        Xo = a1 / ma.sqrt(b1 * BO1 + a1)  # 参考点的横坐标
        Yo = b1 / ma.sqrt(a1 * BO2 + b1)  # 参考点的纵坐标

        AO1 = ma.pow(ma.tan(weidu1), 2)
        AO2 = ma.pow(1 / ma.tan(weidu1), 2)
        Xa = a1 / ma.sqrt(b1 * AO1 + a1)  # 目标点的横坐标
        Ya = b1 / ma.sqrt(a1 * AO2 + b1)  # 目标点的纵坐标
        Y = ma.sqrt(ma.pow(Xa - Xo, 2) + ma.pow(Ya - Yo, 2))  # 目标点与参考点在平面坐标系中纵轴方向的距离
        return Y

    def ToX(self, weidu, jingdu, jingdu1):
        a = 6378137
        b = 6356752

        a1 = ma.pow(a, 2)
        b1 = ma.pow(b, 2)
        BO1 = ma.pow(ma.tan(weidu), 2)
        Xo = a1 / ma.sqrt(b1 * BO1 + a1)
        X = Xo * ma.fabs(jingdu - jingdu1)  # 目标点与参考点之间在平面坐标系中横轴方向上的距离
        return X







def openfile():
    r = askopenfilenames(title='打开文件', filetypes=[('All File', '*')])
    if r != '':
        p = 1
        for num in range(len(r)):
            try:
                if re.match("(.)*.csv$", r[num]) is not None:
                    data = pda.read_csv(r[num])  # 直接对文件路径名及文件进行read 不需要提前打开
                else:
                    data = pda.read_excel(r[num])

            except Exception as e:
                print(tkinter.messagebox.showerror("Error", "第" + str(num + 1) + "张表格报错" + " " + repr(e) + os.linesep))
                break

            try:
                line = len(data.values)
                a = list(data['作业深度(mm)'])
                b = list(data['机具状态'])
                c = list(data['经度'])  # 纬度
                d = list(data['纬度'])  # 经度
                e = c[0]  # 第一个经度
                f = d[0]  # 第一个纬度

                g = GetPoint(e, f)  # 获得参照点

                h = []  # 由纬度转换后的Y轴坐标值
                for i in range(len(c)):
                    h.append(g.ToY(g.latitude, c[i]))
                k = []  # 由经度转换后的X轴坐标值
                for j in range(len(d)):
                    k.append(g.ToX(g.latitude, g.longtitude, d[j]))

                for i in range(line):
                    # 根据机具状态和作业深度进行分割，空行轨迹点视为无效点不进行转换
                    if a[i] == 0 and b[i] == 0:
                        h[i] = 0
                        k[i] = 0
                h.append(0)
                k.append(0)

                m = []
                n = []

                for i in range(len(h)):
                    if h[i] != 0 and k[i] != 0:  # 作业点可被画图
                        m.append(h[i])
                        n.append(k[i])
                    else:
                        if len(m) <= 20 and len(n) <= 20:  # 连续作业点少于20个视为无效作业
                            m = []
                            n = []
                            continue
                        else:
                            plt.plot(m, n, color='k', linewidth=1)
                            plt.axis('off')
                            plt.savefig("E:/tupian4/%d.jpg" % p)
                            plt.close()
                            label1.config(text="生成了%d张图片" % p)
                            p += 1
                            # plt.show()
                            m = []
                            n = []
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
