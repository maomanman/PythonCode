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



def totalTime(fileName):
    """
    计算一块地的总作业时间；
    总作业时间= 各时间段（由不连续的序列号进行分段，信号漂移点导致的序列号间隔不算 时间分段） 之和
    :param filedData: 地块轨迹点文件
    :return: 一块地的总作业时间
    """

    filedData = pda.read_excel('D:/mmm/轨迹数据集/汇总/' + fileName)
    count = filedData.shape[0]  # 获取轨迹点个数

    sumTime = pda.to_timedelta(0)
    flag = 1 # 标志 有 几个时间段
    IndexGapFlag = 0 # 按序列号不连续分段 的 段落数
    TimeGapFlag = 0 # 按序列号连续 时间间隔不连续分段 的 段落数
    IndexGapList=[] # 收集按序列号不连续分段 的节点间时长
    TimeGapList = []# 收集序列号连续 时间间隔不连续分段  的节点间时长
    timeParaIndex = []  # 收集各个时间段的起止索引号
    startPoint = 0 # 一段连续时间起始的索引
    for i in range(1,count):
        indexGap = filedData.loc[i,'序列号'] -filedData.loc[i-1,'序列号'] # 计算相邻两点间的序列号之差
        # 计算相邻点时间差
        point0 = filedData.loc[i - 1, 'GPS时间']
        point1 = filedData.loc[i, 'GPS时间']
        if type(point1) == str:
            point0 = pda.Timestamp(point0)
            point1 = pda.Timestamp(point1)
        gapT = point1 - point0

        if  indexGap > 2 : # 排除由 信号漂移点导致的时间分段
            endPoint = i-1 # 一段连续时间结束的索引 （因为当前点与前一个点的序号已经分段，那么前一段时间的结束点就是上一个点）
            # 计算此段时间差
            t1 = filedData.loc[startPoint, 'GPS时间']
            t2 = filedData.loc[endPoint, 'GPS时间']
            if type(t2) == str:
                t1 = pda.Timestamp(t1)
                t2 = pda.Timestamp(t2)

            paraGapT = t2 - t1
            timeParaIndex.append((filedData.loc[startPoint, '序列号'], filedData.loc[endPoint, '序列号']))
            IndexGapList.append(gapT)
            sumTime = sumTime + paraGapT
            startPoint = i
            flag = flag +1 # 标志几个时间段
            IndexGapFlag = IndexGapFlag +1


        else : # 序列号连续，时间间隔不连续
            if gapT.total_seconds() > 300: # 间隔时间超过5分钟，则认为时间分段
                endPoint = i - 1  # 一段连续时间结束的索引 （因为当前点与前一个点的序号已经分段，那么前一段时间的结束点就是上一个点）
                # 计算此段时间差
                t1 = filedData.loc[startPoint, 'GPS时间']
                t2 = filedData.loc[endPoint, 'GPS时间']
                if type(t2) == str:
                    t1 = pda.Timestamp(t1)
                    t2 = pda.Timestamp(t2)

                paraGapT = t2 - t1
                timeParaIndex.append((filedData.loc[startPoint, '序列号'], filedData.loc[endPoint, '序列号']))
                TimeGapList.append(gapT)
                sumTime = sumTime + paraGapT
                startPoint = i
                flag = flag + 1  # 标志几个时间段
                TimeGapFlag = TimeGapFlag + 1


    # 只有一个时间段 或 多个时间段的最后一个时间的时长计算
    endPoint = count-1
    t1 = filedData.loc[startPoint, 'GPS时间']
    t2 = filedData.loc[endPoint, 'GPS时间']
    if type(t2) == str:
        t1 = pda.Timestamp(t1)
        t2 = pda.Timestamp(t2)
    gapT = t2 - t1
    sumTime =sumTime + gapT
    timeParaIndex.append((filedData.loc[startPoint, '序列号'], filedData.loc[endPoint, '序列号']))


    # print(flag)
    # return sumTime,flag,gapList
    return sumTime,flag,IndexGapFlag,TimeGapFlag,IndexGapList,TimeGapList,timeParaIndex


def batchTotalTime():
    """
    批量计算每个文件的总时长，并登记保存
    :return:
    """
    rootP = r'D:\mmm\实验数据\test21'
    test21Data = pda.read_excel(rootP + '/test21-轨迹索引-v1.0.xlsx')

    test21_result_info = pda.DataFrame(columns=['文件名称','总工作时长','时间段数','序列号分段节点数','时间间隔分段节点数','序列号分段各节点的时间差','时间间隔分段各节点的时间差','各个时间段起止序列号'])

    for i in test21Data.index:
        fileName = test21Data.loc[i,'文件名称']
        sumTime,timeNum,indexGapNum,timeGapNum ,IndexGapList,TimeGapList,timeParaIndex= totalTime(fileName)
        test21_result_info.loc[i]=[fileName,str(sumTime),timeNum,indexGapNum,timeGapNum,IndexGapList,TimeGapList,timeParaIndex]
        if i % 10 == 0 :
            test21_result_info.to_excel(rootP+'/test21_result_info.xlsx')


    test21_result_info.to_excel(rootP + '/test21_result_info.xlsx')



#########################################################################################################
# test21()

# path = r'D:\mmm\实验数据\test15\edgePoint'
# # # 189_edge.xlsx edgePointInfo_0618164810.xlsx  mokat.xlsx 00189_edgePoint_R=5.8.xlsx
# edge = pda.read_excel(path+'/00022_edgePoint_R=9.19.xlsx')
# # # edge = pda.read_csv(path+'/edge_0618164108.csv')
# #
# area = selfShape.calFiledArea(edge)
# print(area)

# mokatuo = pda.DataFrame(columns=['xy'])
# x_y=WGS84ToWebMercator(np.array(edge))
# for i,pt in enumerate(x_y):
#     # print('{:.3f} {:.3f}'.format(*pt))
#     mokatuo.loc[i]='{:.3f} {:.3f}'.format(*pt)
#
# mokatuo.to_excel(path+'/mokat.xlsx')

# 00169 耕-中-绕==鲁16-543101_2020-10-31==1031-0522-filed.xlsx
# 00001 耕-大-套==黑02-452C12_2016-10-9==1009-0125-filed.xls
# tt = totalTime("00001 耕-大-套==黑02-452C12_2016-10-9==1009-0125-filed.xls")
# print('总工作时间：{}'.format(tt))

batchTotalTime()