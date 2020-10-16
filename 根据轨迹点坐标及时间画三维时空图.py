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
import matplotlib.dates as mdates
from mpl_toolkits.mplot3d import Axes3D
import tkinter.messagebox
from tkinter.filedialog import *
import time
import os

#  自己的模块
from SplitFileByMoreAttributes_20200925_v3_0 import *


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
                # data, h, k, shape_x, shape_y = SplitfieldByMoreAtrributes(data, r[num])
                # m = []
                # n = []
                h = list(data.loc[:, 'x'])
                k = list(data.loc[:, 'y'])
                # t= str(data.loc[:,'GPS时间'])
                # str(h)
                # z=npy.linspace(0, data.shape[0]*2-2, data.shape[0])
                z = data.loc[:,'GPS时间']

                fig = plt.figure()
                ax = fig.gca(projection='3d')
                # ax.zaxis_date(z)
                ax.zaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
                # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H'))
                # p = 1  # 用于图片命名，与地块标志相对应

                ax.plot(h, k, z, label='parametric curve')
                ax.legend()

                plt.show()


                # count = 1  # 用于计算图片数量
                # fileName = r[num]
                # fileName = fileName.split('.')
                # # fileName = fileName[0] + '-tupian/'
                # # os.mkdir(fileName)
                #
                # indexOfA = [i for i, x in enumerate(h) if x == 'a']
                # i = 0
                # while i < len(indexOfA):
                #     if i == 0 and indexOfA[i] > 20:
                #         m = h[0:indexOfA[i]]
                #         n = k[0:indexOfA[i]]
                #     elif i != 0 and indexOfA[i] - indexOfA[i - 1] - 1 > 20:
                #         m = h[indexOfA[i - 1] + 1:indexOfA[i]]
                #         n = k[indexOfA[i - 1] + 1:indexOfA[i]]
                #     else:
                #         i += 1
                #         p += 1
                #         continue
                # plt.plot(k, h, color='k', linewidth=1)
                # plt.axis('off')
                # plt.savefig(fileName[0] + '-{}.jpg'.format(p))
                # plt.close()
                #     label1.config(text="生成了%d张图片" % count)
                #     p += 1
                #     count += 1
                #     i += 1
                #     # del m, n, sh_x, sh_y

            except Exception as e:
                print(tkinter.messagebox.showerror("Error", "第" + str(num + 1) + "张表格报错" + " " + repr(e) + os.linesep))
            '''g = open('mistake.txt','a+')
            g.write("第"+str(num+1)+"张表格报错"+" "+repr(e)+os.linesep)
            g.close()'''
            continue
            del data


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
