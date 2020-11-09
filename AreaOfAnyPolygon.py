import  pandas as pad
import os
import time
import math as ma


# 任意多边形的面积计算
areaInfo = pad.DataFrame(columns=['filename','edgeNum','area(平方米)','area(亩)','面积计算时间'])
ai = 0
path ='D:/mmm/轨迹数据集/地块/按作业模式分类/just/edge-R=6625'
fns = [fn for fn in os.listdir(path) if fn.endswith('.csv')]
for fn in fns :
    filepath = path + '/' + fn
    edge = pad.read_csv(filepath)

    count = edge.shape[0]-1
    i = 0
    temp = 0
    area = 0
    # 多边形面积计算
    start = time.time()
    while i < count:
        temp += edge.x[i]* edge.y[i+1] - edge.x[i+1]*edge.y[i]
        i += 1
    area = 0.5 * ma.fabs(temp)  # 平方米  （多边形顶点按逆时针排列则是正值，顺时针排列则是负值）
    end = time.time()

    s =  area* 0.0015 # 亩
    areaInfo.loc[ai]=[fn,count,area,s, end- start]
    ai +=1
    del edge

areaInfo.to_excel(path + '/areaInfo.xlsx')