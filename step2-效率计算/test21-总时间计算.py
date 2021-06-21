import pandas as pda
import numpy as np
import math
import datetime
import time

import alpha_shape.AlphaShapeForEdge as selfShape
from alpha_shape.ZuoBiaoZhuanHuan import LatLon2GSXY
from alpha_shape.ZuoBiaoZhuanHuan import WGS84ToWebMercator




def test21():
    """
    检查轨迹文件中是否存在两点距离较近而时间间隔较远的情况
    :return:
    """
    rootP = r'D:\mmm\实验数据\test21'
    fileP = r'D:\mmm\轨迹数据集\汇总'
    testfile = 'test21-轨迹索引-v1.0.xlsx'

    testfiledata = pda.read_excel(rootP + '/' + testfile)
    testfiledata.set_index('新文件序号', inplace=True)
    # returnfile = pda.DataFrame(
    #     columns=['文件名称', '连续点的最长时间间隔','连续点的距离','连续点序列号起', '连续点序列号止', '不连续点的最长时间间隔','不连续点的距离', '不连续点序列号起', '不连续点序列号止'])

    returnfile = pda.DataFrame(columns=['文件名称','点个数','首位序列号之差','空缺的点个数'])

    flag = time.strftime("%m%d%H%M%S", time.localtime())

    newid = 0
    for fid in testfiledata.index:
        filename = testfiledata.loc[fid, '文件名称']
        # filedata = pda.read_excel(fileP + '/' + filename)
        filedata =selfShape.GetData(fileP + '/' + filename)
        # filedata = filedata[filedata.工作状态 == True]
        # filedata.reset_index(drop=True,inplace=True)
        #
        print(filename)
        # yangTime = selfShape.calYangTime(filedata)
        yangT = testfiledata.loc[fid,'采样时间']

        print(yangT)
        #
        count = filedata.shape[0]
        # 先计算相邻两点的时间间隔
        maxSerY = datetime.timedelta()  # 序列号连续的两点间的最大时间间隔
        maxY = datetime.timedelta()  # 序列号不连续的两点间的最大时间间隔
        serIndStart = 0
        serIndEnd = 0
        serDis =0
        notSerIndStart = 0
        notSerIndEnd = 0
        dis=0
        # for ind in range(1, count):
        #     t1 = filedata.loc[ind - 1, 'GPS时间']
        #     t2 = filedata.loc[ind, 'GPS时间']
        #     if type(t2) == str:
        #         t1 = pda.Timestamp(t1)
        #         t2 = pda.Timestamp(t2)
        #         gapT = t2 - t1
        #     else:
        #         gapT = t2 - t1

        gap= filedata.loc[count - 1, '序列号']-filedata.loc[0, '序列号'] +1
        returnfile.loc[newid] = [filename, count,gap,gap - count]
        if newid % 10 == 0:
            returnfile.to_excel(rootP + '/test21_returnfile_' + flag + '_序列号之差.xlsx')
        newid = newid + 1


            #
            # if filedata.loc[ind, '序列号'] - filedata.loc[ind - 1, '序列号'] != 1:
            #     # 序列号连续
            #     if int(gapT.total_seconds()) != yangT:
            #         serIndStart = filedata.loc[ind - 1, '序列号']
            #         serIndEnd = filedata.loc[ind, '序列号']
            #         serDis = selfShape.distance((filedata.loc[ind, 'x'], filedata.loc[ind, 'y']),
            #                                     (filedata.loc[ind - 1, 'x'], filedata.loc[ind - 1, 'y']))
            #         returnfile.loc[newid] = [filename, str(gapT), serDis, serIndStart, serIndEnd, str(maxY), dis,
            #                                  notSerIndStart, notSerIndEnd]
            #         if newid % 10 == 0:
            #             returnfile.to_excel(rootP + '/test21_returnfile_' + flag + '.xlsx')
            #         newid = newid + 1

                # if gapT > maxSerY:
                #     maxSerY = gapT
                #     serIndStart = filedata.loc[ind - 1, '序列号']
                #     serIndEnd = filedata.loc[ind, '序列号']
                #     # 计算两点间距离
                #     serDis = selfShape.distance((filedata.loc[ind, 'x'],filedata.loc[ind, 'y']), (filedata.loc[ind - 1, 'x'],filedata.loc[ind - 1, 'y']))
            # else:
            #     # 序列号不连续
            #     if gapT > maxY:
            #         maxY = gapT
            #         notSerIndStart = filedata.loc[ind - 1, '序列号']
            #         notSerIndEnd = filedata.loc[ind, '序列号']
            #         # 计算两点间距离
            #         dis=selfShape.distance((filedata.loc[ind, 'x'],filedata.loc[ind, 'y']), (filedata.loc[ind - 1, 'x'],filedata.loc[ind - 1, 'y']))



        # returnfile.loc[newid]= [filename, str(maxSerY), serDis,serIndStart, serIndEnd, str(maxY), dis,notSerIndStart, notSerIndEnd]
        # returnfile.loc[newid] =[filename,yangTime]



    returnfile.to_excel(rootP + '/test21_returnfile_'+flag+'.xlsx')




# test21()

path = r'D:\mmm\实验数据\小汤山实验准备'
# # 189_edge.xlsx edgePointInfo_0618164810.xlsx  mokat.xlsx 00189_edgePoint_R=5.8.xlsx
edge = pda.read_excel(path+'/mokat.xlsx')
# # edge = pda.read_csv(path+'/edge_0618164108.csv')
#
area = selfShape.calFiledArea(edge)
print(area)

# mokatuo = pda.DataFrame(columns=['xy'])
# x_y=WGS84ToWebMercator(np.array(edge))
# for i,pt in enumerate(x_y):
#     # print('{:.3f} {:.3f}'.format(*pt))
#     mokatuo.loc[i]='{:.3f} {:.3f}'.format(*pt)
#
# mokatuo.to_excel(path+'/mokat.xlsx')