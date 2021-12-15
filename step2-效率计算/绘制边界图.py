import pandas as pda
import numpy as np
import math
import datetime
import time
import matplotlib.pyplot as plt
import alpha_shape.AlphaShapeForEdge as selfShape


def plotEdge(savePath, imformat='svg'):
    filename = '00762 收-小-绕==皖13-00562_2020-6-6==0606-0806-filed.xlsx  '
    edgeFile = '00762_edgePoint_R=8.81.xlsx'

    path = r'D:\mmm\轨迹数据集\汇总'
    edgeP = 'D:\mmm\轨迹数据集\轨迹图汇总\edgePoint'

    data = selfShape.GetData(path + '/' + filename)
    edgeData = pda.read_excel(edgeP + '/' + edgeFile)

    selfShape.plotEdgefor12(data, edgeData.x, edgeData.y, savePath, imformat)


def plotPie():
    """
    绘制饼图
    :return:
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']

    plt.figure(figsize=(9, 6), dpi=100)
    # x = [332, 390, 326, 15]
    # labels = ['绕行法', '梭行法','套行法',  '斜行法']

    x=[282,289,492]
    labels =['小块面积','中等面积','大块面积']
    _,_,autotexts=plt.pie(x=x,labels=labels,autopct='%.lf%%',colors=['#e377c2', '#7f7f7f', '#bcbd22'])
    for autotext in autotexts:
        autotext.set_color('white')
    # plt.title('作业模式计数饼图')
    # plt.legend(labels,loc='lower left')
    plt.savefig(r'D:\mmm\参考文献\我的小论文\小论文插图\8-面积尺度计数饼图.svg', format='SVG', dpi=500)
    # plt.show()



plotEdge(savePath=r'D:\mmm\参考文献\我的小论文\小论文插图\6-762关机停歇示意图.svg', imformat='SVG')
# plotPie()

# selfShape.justShowEdge('00653 耕-小-绕==湘08-20012_2016-11-5==1105-0717-filed.xlsx',8.34)