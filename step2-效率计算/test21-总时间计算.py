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

def aFileNoWorkTime(fileName, yangT, paraTimeList):
    """
    获得一个地块轨迹文件的有效工作时间：根据工作状态判断
    :param fileName: 轨迹文件名
    :param yangT: 采样时间
    :param paraTimeList: 时间段起止序列号的列表
    :return: 有效工作时间
    """
    fileData = pda.read_excel('D:/mmm/轨迹数据集/汇总/' + fileName)

    paraNum = len(paraTimeList)  # 时间段个数
    sumWorkTime = pda.to_timedelta(0)
    numList = []
    gapIndCountListList=[]
    gapIndParaListList=[]

    for i in range(0, paraNum):
        # 获取 时间段 起止序列号
        startPoint = int(paraTimeList[i].split(', ')[0])
        endPoint = int(paraTimeList[i].split(', ')[1])

        # 获取时间段轨迹点数据
        paraData = fileData[fileData['序列号'] >= startPoint]
        paraData = paraData[paraData['序列号'] <= endPoint]

        # paraTime = paraNoWorkTime(paraData, yangT)
        num, gapIndCountList, gapIndParaList=paraNoWorkTime(paraData, yangT)
        numList.append(num)
        gapIndCountListList.append(gapIndCountList)
        gapIndParaListList.append(gapIndParaList)

        # sumWorkTime = sumWorkTime + paraTime
        # print(i)
    return numList,gapIndCountListList,gapIndParaListList
    # return sumWorkTime
def paraNoWorkTime(paraData, yangT):
    """
    计算一段时间段内的有效工作时长：在计算总时长的基础上加上对工作属性的限定
    :param paraData: 一段时间内的轨迹点
    :param yangT: 采样时间
    :return: 这段时间内的有效工作时长
    """
    # yangT = pda.to_timedelta(yangT, unit='s')
    paraData = paraData[paraData['工作状态'] == False]  # 筛选非工作点
    paraData.reset_index(drop=True, inplace=True)
    count = paraData.shape[0]

    # returnfile = pda.DataFrame(columns=['文件名称', '连续点个数', '起止序列号','时间差'])

    maxNum = 300/yangT

    sumTime = pda.to_timedelta(0)
    startPoint = 0
    gapIndCount = 1
    gapIndCountList = []
    gapIndParaList = []
    num = 0
    for ind in paraData.index:
        if ind == 0:
            continue

        # 判断序列号是否连续
        gapInd = paraData.loc[ind, '序列号'] - paraData.loc[ind - 1, '序列号']
        if gapInd > 1:  # 序列号不连续
            if gapIndCount > maxNum :
                # returnfile.loc[]=
                num = num + 1
                gapIndCountList.append(gapIndCount)
                t1 = paraData.loc[ind-1, 'GPS时间']
                t2 = paraData.loc[ind-gapIndCount, 'GPS时间']
                if type(t1) == str:
                    t1 = pda.Timestamp(t1)
                    t2 = pda.Timestamp(t2)
                gapTime = t1-t2
                gapIndParaList.append(gapTime)
            gapIndCount = 1


            # endPoint = ind - 1
            #
            # # 计算此段时间差
            # t1 = paraData.loc[startPoint, 'GPS时间']
            # t2 = paraData.loc[endPoint, 'GPS时间']
            # if type(t2) == str:
            #     t1 = pda.Timestamp(t1)
            #     t2 = pda.Timestamp(t2)
            # paraGapT = t2 - t1
            # if paraGapT.total_seconds() == 0:  # 孤立的一个工作点,其工作时间记为采样时间
            #     paraGapT = yangT
            # sumTime = sumTime + paraGapT
            #
            # startPoint = ind  # 下一个连续时间段的起始点
        else:
            gapIndCount = gapIndCount +1

    # if count > 0:
    #     endPoint = count - 1
    #
    #     if endPoint == startPoint:
    #         paraGapT = yangT
    #     else:
    #         # 计算此段时间差
    #         t1 = paraData.loc[startPoint, 'GPS时间']
    #         t2 = paraData.loc[endPoint, 'GPS时间']
    #         if type(t2) == str:
    #             t1 = pda.Timestamp(t1)
    #             t2 = pda.Timestamp(t2)
    #         paraGapT = t2 - t1
    #
    #     sumTime = sumTime + paraGapT

    if gapIndCount > maxNum :
        num = num + 1
        gapIndCountList.append(gapIndCount)
        t1 = paraData.loc[ind - 1, 'GPS时间']
        t2 = paraData.loc[ind - gapIndCount, 'GPS时间']
        if type(t1) == str:
            t1 = pda.Timestamp(t1)
            t2 = pda.Timestamp(t2)
        gapTime = t1 - t2
        gapIndParaList.append(gapTime)


    # return sumTime
    return  num,gapIndCountList,gapIndParaList
def batchGetNoWorkTime():
    """
    批量获取所有地块作业时间
    :return:
    """

    rootPath = r'D:\mmm\实验数据\test23-中期信息整理'
    # 通过索引表获取 各个文件的 文件名、采样时间
    fileIndexData = pda.read_excel(rootPath + '/test23-轨迹索引-v2.0.xlsx')

    # 读取 test21  的 结果表，获取各个时间段的起止序列号列表
    test22_ParaTimeList = pda.read_excel(rootPath + '/test23-总时间统计.xlsx')

    test22_return_info = pda.DataFrame(columns=['文件名称','num','gapIndCountListList','gapIndParaListList'])

    for ind in fileIndexData.index:
        fileName = fileIndexData.loc[ind, '文件名称']
        if fileName == test22_ParaTimeList.loc[ind, '文件名称']:
            # print(fileName)
            # print(test22_ParaTimeList.loc[ind,'文件名称'])
            # print('\n')
            # print(fileIndexData.loc[ind,'新文件序号'])
            yangT = fileIndexData.loc[ind, '采样时间']
            paraTimeL = test22_ParaTimeList.loc[ind, '各个时间段起止序列号']  # 是一个字符串

            paraTimeL = paraTimeL.split('), (')
            paraTimeL[0] = paraTimeL[0].replace('[(', '')
            paraTimeL[len(paraTimeL) - 1] = paraTimeL[len(paraTimeL) - 1].replace(')]', '')
            # print(paraTimeL)
            numList,gapIndCountListList,gapIndParaListList = aFileNoWorkTime(fileName, yangT, paraTimeL)
            # totalTime = test22_ParaTimeList.loc[ind, '总工作时长']

            test22_return_info.loc[ind] = [fileName, numList,gapIndCountListList,gapIndParaListList]

        if ind % 10 == 0:
            test22_return_info.to_excel(rootPath + '/test21_开机停歇统计情况.xlsx')

    test22_return_info.to_excel(rootPath + '/test21_开机停歇统计情况.xlsx')


def aFileLongTimeNoWork(fileName, yangT=2):
    """
    开机停歇情况的 统计：
    1、筛选出非工作点
    2、登记 连续非工作点个数、连续非工作时长、连续非工作平均速度 ；（对于存在序列号连续的关机停歇情况进行按不连续处理）
    :param fileName:地块文件名
    :param yangT:暂时未用到
    :return:
    """
    fileData = pda.read_excel('D:/mmm/轨迹数据集/汇总/' + fileName)
    fileData = fileData[fileData['工作状态'] == False]  # 筛选非工作点
    fileData.reset_index(drop=True, inplace=True)

    registerFile = pda.DataFrame(columns=['文件名称','连续点个数','起止序号','时间差','平均速度'])

    continuousNum  = 1 # 连续点个数
    i= 0
    for ind in fileData.index:
        if ind == 0 :
            continue
        # 判断序列号是否连续
        gapInd = fileData.loc[ind, '序列号'] - fileData.loc[ind - 1, '序列号']

        if gapInd > 2: # 不连续(存在删除信号漂移点导致的序列号间隔为2）
            if continuousNum > 1 :
                # 计算时间差
                t1 = fileData.loc[ind - 1, 'GPS时间']
                t2 = fileData.loc[ind - continuousNum, 'GPS时间']
                if type(t1) == str:
                    t1 = pda.Timestamp(t1)
                    t2 = pda.Timestamp(t2)
                gapTime = t1 - t2
                # 计算平均速度
                vec = fileData.loc[ind - continuousNum:ind - 1,'速度(km/h)'].sum()/continuousNum
                registerFile.loc[i] = [fileName,continuousNum,[fileData.loc[ind- continuousNum, '序列号'] ,fileData.loc[ind - 1, '序列号']],str(gapTime),vec]
                i = i + 1
                continuousNum = 1

        else: # 序列号连续
            # 计算相邻点时间差
            point0 = fileData.loc[ind - 1, 'GPS时间']
            point1 = fileData.loc[ind, 'GPS时间']
            if type(point1) == str:
                point0 = pda.Timestamp(point0)
                point1 = pda.Timestamp(point1)
            gapT = point1 - point0

            # 判断是否存在关机停歇情况
            if gapT.total_seconds() > 300:  # 相邻点间隔时间超过5分钟，则认为是关机停歇情况
                # 计算时间差
                t1 = fileData.loc[ind - 1, 'GPS时间']
                t2 = fileData.loc[ind - continuousNum, 'GPS时间']
                if type(t1) == str:
                    t1 = pda.Timestamp(t1)
                    t2 = pda.Timestamp(t2)
                gapTime = t1 - t2
                # 计算平均速度
                vec = fileData.loc[ind - continuousNum:ind - 1, '速度(km/h)'].sum() / continuousNum
                registerFile.loc[i] = [fileName, continuousNum,
                                       [fileData.loc[ind - continuousNum, '序列号'], fileData.loc[ind - 1, '序列号']],
                                       str(gapTime), vec]
                i = i + 1
                continuousNum = 1
            else:
                continuousNum = continuousNum+ 1

    if continuousNum > 1 :
        # 计算时间差
        t1 = fileData.loc[ind , 'GPS时间']
        t2 = fileData.loc[ind - continuousNum+1, 'GPS时间']
        if type(t1) == str:
            t1 = pda.Timestamp(t1)
            t2 = pda.Timestamp(t2)
        gapTime = t1 - t2
        # 计算平均速度
        vec = fileData.loc[ind - continuousNum+1:ind,'速度(km/h)'].sum()/continuousNum
        registerFile.loc[i] = [fileName,continuousNum,[fileData.loc[ind- continuousNum+1, '序列号'] ,fileData.loc[ind , '序列号']],str(gapTime),vec]
        i = i + 1
    # registerFile.to_excel(r'D:\mmm\实验数据\test21-总作业时长\开机停歇' + '/registerFile_00023.xlsx')
    return registerFile

def batchLongTimeNoWork():
    """
    批量统计关机停歇情况数据
    :return:
    """

    rootP = r'D:\mmm\实验数据\test21-总作业时长\开机停歇'
    test21Data = pda.read_excel(rootP + '/test21-轨迹索引-v2.0.xlsx')

    registerFile = pda.DataFrame(columns=['文件名称', '连续点个数', '起止序号', '时间差', '平均速度'])

    for i in test21Data.index:
        fileName = test21Data.loc[i, '文件名称']
        yangT = test21Data.loc[i,'采样时间']

        returnData = aFileLongTimeNoWork(fileName,yangT)
        registerFile = registerFile.append(returnData)

        if i % 10 == 0:
            registerFile.to_excel(rootP + '/test21-关机停歇情况统计.xlsx')

    registerFile.to_excel(rootP + '/test21-关机停歇情况统计.xlsx')

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
    rootP = r'D:\mmm\实验数据\test23-中期信息整理'
    test21Data = pda.read_excel(rootP + '/test23-轨迹索引-v2.0.xlsx')

    test21_result_info = pda.DataFrame(columns=['文件名称','总工作时长','时间段数','序列号分段节点数','时间间隔分段节点数','序列号分段各节点的时间差','时间间隔分段各节点的时间差','各个时间段起止序列号'])

    for i in test21Data.index:
        fileName = test21Data.loc[i,'文件名称']
        sumTime,timeNum,indexGapNum,timeGapNum ,IndexGapList,TimeGapList,timeParaIndex= totalTime(fileName)
        test21_result_info.loc[i]=[fileName,str(sumTime),timeNum,indexGapNum,timeGapNum,IndexGapList,TimeGapList,timeParaIndex]
        if i % 10 == 0 :
            test21_result_info.to_excel(rootP+'/test23-中期汇总_总时间统计.xlsx')


    test21_result_info.to_excel(rootP + '/test23-中期汇总_总时间统计.xlsx')



############## 除去 开机停歇 、关机停歇、 分段处理的 时间##########################################
def getWorkTime(fileData,startIndex,endIndex,yangT):
    """
    获取 从 indStart 开始的到 indEnd 结束的时长
    :param fileData:  地块文件
    :param startIndex: 计算时长的起始索引号
    :param endIndex: 计算时长的结束索引号
    :param yangT: 采样时间
    :return: 返回这段序列号的时间差
    """
    if startIndex == endIndex:
        workTime = pda.to_timedelta(yangT, unit='s')
    else:
        t1 = fileData.loc[startIndex, 'GPS时间']
        t2 = fileData.loc[endIndex, 'GPS时间']
        if type(t1) == str:
            t1 = pda.Timestamp(t1)
            t2 = pda.Timestamp(t2)
        workTime = t2 - t1
    return workTime

def IsbootUpStopPara(fileData,startIndex,endIndex,timeThrehold ,speedThrehold):
    """
    判断这段估计是否为 关机停歇点
    :param fileData: 地块文件
    :param startIndex: 连续非工作点的起始索引号
    :param endIndex: 连续非工作点的结束索引号
    :param timeThrehold: 关机停歇时间阈值 ，单位秒，默认按 5分钟=300秒 计算
    :param speedThrehold: 关机停歇速度阈值 ，单位km/h，默认按 1km/h 计算
    :return: True : 是开机停歇点;False :不是开机停歇点
    """

    # 判断这些连续非工作点是否为 关机停歇点
    # 计算时间差
    t1 = fileData.loc[startIndex, 'GPS时间']
    t2 = fileData.loc[endIndex, 'GPS时间']
    if type(t1) == str:
        t1 = pda.Timestamp(t1)
        t2 = pda.Timestamp(t2)
    gapTime = t2 - t1
    # 计算平均速度
    aveSpeed = fileData.loc[startIndex:endIndex, '速度(km/h)'].sum() / (endIndex-startIndex+1)

    if gapTime.total_seconds() > timeThrehold and aveSpeed < 1:  # 连续非工作时长大于 停歇时间阈值   并且，平均速度小于 速度阈值
        return True
    else:
        return False


def bootUpParaWorkTime(fileData,startIndex,endIndex,yangT,timeThrehold,speedThrehold):
    """
    判断该序列号段内(序列号要连续)是否存在 开机停歇情况，有则将此停歇时间剔除，最后计算该序号段内的总工作时长
    开机停歇：序列号连续，工作状态为非工作模式，且速度较小；通过停歇时间和速度设置阈值进行筛选
    :param fileData: 地块轨迹文件
    :param startIndex:开始索引号
    :param endIndex:结束索引号
    :param yangT:采样时间
    :param timeThrehold: 开机停歇时间阈值 ，单位秒，默认按 5分钟=300秒 计算
    :param speedThrehold: 开机停歇速度阈值 ，单位km/h，默认按 1km/h 计算
    :return: 该段轨迹的工总工作时长
    """


    paraData = fileData.loc[startIndex:endIndex]
    iStart = startIndex
    indEnd = endIndex
    paraData = paraData[paraData['工作状态']==False]
    paraData.reset_index(inplace=True)
    paraPointNum =paraData.shape[0]

    noWorkPointNum = 1
    workTime = pda.to_timedelta(0)

    for ind in range(1,paraPointNum):

        gapInd = paraData.loc[ind, '序列号'] - paraData.loc[ind - 1, '序列号']
        if gapInd > 2 or (gapInd==2 and paraData.loc[ind, '序列号']-1 in list(fileData.序列号)):  # 不连续(存在删除信号漂移点导致的序列号间隔为2）


            if noWorkPointNum > 1: # 存在连续非工作点
                paraStartIndex=paraData.loc[ind - noWorkPointNum, 'index']  # 连续非工作点的起始索引号
                paraEndIndex =paraData.loc[ind - 1, 'index'] # 连续非工作点的结束索引号
                if IsbootUpStopPara(fileData,paraStartIndex,paraEndIndex,timeThrehold ,speedThrehold): # 判断是否是开机停歇点
                    iEnd = paraData.loc[ind - noWorkPointNum, 'index']-1

                    if iEnd>=iStart:
                        if debugFlag:
                            print("\t\tbootUpParaWorkTime:1-iStart = %d,iEnd=%d" % (fileData.loc[iStart,'序列号'], fileData.loc[iEnd,'序列号']))
                        wt = getWorkTime(fileData,iStart,iEnd,yangT)
                        workTime = workTime + wt

                    iStart = paraData.loc[ind - 1, 'index'] + 1  # 关机停歇后 的下一个点是下一段工作时间段的开始点


                noWorkPointNum = 1

        else:  # 序列号连续
            noWorkPointNum =  noWorkPointNum + 1

    # print(noWorkPointNum)
    if noWorkPointNum > 1: #最后一个点
        paraStartIndex = paraData.loc[ind - noWorkPointNum+1, 'index']  # 连续非工作点的起始索引号
        paraEndIndex = paraData.loc[ind, 'index']  # 连续非工作点的结束索引号
        if IsbootUpStopPara(fileData, paraStartIndex, paraEndIndex, timeThrehold, speedThrehold):  # 判断是否是开机停歇点
            iEnd = paraData.loc[ind - noWorkPointNum+1, 'index']-1

            if iEnd>=iStart: # 开机停歇非首段，跳过开机停歇部分计算iStart到停歇开始部分的工作时长
                wt = getWorkTime(fileData, iStart, iEnd,yangT)
                if debugFlag:
                    print("\t\tbootUpParaWorkTime:2-iStart = %d,iEnd=%d" % (fileData.loc[iStart,'序列号'], fileData.loc[iEnd,'序列号']))
                workTime = workTime + wt

            iStart = paraData.loc[ind, 'index'] + 1  # 开机停歇后 的下一个点是下一段工作时间段的开始点

        if iStart <= endIndex:
            iEnd =endIndex
            wt = getWorkTime(fileData, iStart, iEnd, yangT)
            workTime = workTime + wt
            if debugFlag:
                print("\t\tbootUpParaWorkTime:3-iStart = %d,iEnd=%d" % (fileData.loc[iStart,'序列号'], fileData.loc[iEnd,'序列号']))
    else:
        iEnd = endIndex
        wt = getWorkTime(fileData, iStart, iEnd,yangT)
        workTime = workTime + wt
        if debugFlag:
            print("\t\tbootUpParaWorkTime:4-iStart = %d,iEnd=%d" % (fileData.loc[iStart,'序列号'], fileData.loc[iEnd,'序列号']))

    return workTime


def shutDownParaWorkTime(fileData,startIndex,endIndex,yangT,timeThrehold ,speedThrehold):
    """
    判断该序列号段内(序列号要连续)是否存在 关机停歇情况（序列号连续，时间间隔大），有则将此停歇时间剔除，最后计算该序号段内的总工作时长
    :param fileData: 地块轨迹文件
    :param startIndex:开始索引号
    :param endIndex:结束索引号
    :param yangT:采样时间
    :param timeThrehold: 关机停歇时间阈值 ，单位秒，默认按 5分钟=300秒 计算
    :param speedThrehold: 关机停歇速度阈值 ，单位km/h，默认按 1km/h 计算
    :return: 该段轨迹的工总工作时长
    """
    # debugFlag = 1

    paraData = fileData.loc[startIndex:endIndex]
    paraData.reset_index(inplace = True)
    iStart = startIndex

    paraPointNum = paraData.shape[0]
    workTime = pda.to_timedelta(0)

    for ind in range(1,paraPointNum):
        # 计算相邻点时间差
        point0 = paraData.loc[ind - 1, 'GPS时间']
        point1 = paraData.loc[ind, 'GPS时间']
        if type(point1) == str:
            point0 = pda.Timestamp(point0)
            point1 = pda.Timestamp(point1)
        gapT = point1 - point0
        # 判断是否存在关机停歇情况
        if gapT.total_seconds() > timeThrehold:  # 相邻点间隔时间超过5分钟，则认为是关机停歇情况
            iEnd = paraData.loc[ind, 'index'] - 1
            if debugFlag:
                print("\tshutDownParaWorkTime :1=iStart=%d,iEnd=%d" % (fileData.loc[iStart,'序列号'], fileData.loc[iEnd,'序列号']))
            wt = bootUpParaWorkTime(fileData, iStart, iEnd, yangT, timeThrehold, speedThrehold)
            workTime = workTime  + wt
            iStart = paraData.loc[ind, 'index']


    iEnd = endIndex
    if debugFlag:
        print("\tshutDownParaWorkTime:2=iStart=%d,iEnd=%d"%(fileData.loc[iStart,'序列号'], fileData.loc[iEnd,'序列号']))
    wt = bootUpParaWorkTime(fileData, iStart, iEnd, yangT, timeThrehold, speedThrehold)
    workTime = workTime + wt
    return workTime

def indexDisContinuous(fileData,yangT,timeThrehold ,speedThrehold):
    """
    判断该文件是否存在 序列号不连续 的情况 ，有则将此段时间剔除，最后计算该序号段内的总工作时长
    :param fileData: 地块轨迹文件
    :param yangT:采样时间
    :param timeThrehold: 关机停歇时间阈值 ，单位秒，默认按 5分钟=300秒 计算
    :param speedThrehold: 关机停歇速度阈值 ，单位km/h，默认按 1km/h 计算
    :return: 该段轨迹的工总工作时长
    """
    # debugFlag = 1

    iStart = 0
    workTime = pda.to_timedelta(0)
    pointNum = fileData.shape[0]

    for ind in range(1,pointNum):
        index1 = fileData.loc[ind,'序列号']
        index2 = fileData.loc[ind-1, '序列号']

        if index1-index2 > 1:
            iEnd = ind - 1
            if debugFlag:
                print("\nindexDisContinuous : 1-iStart=%d,iEnd=%d" % (fileData.loc[iStart,'序列号'], fileData.loc[iEnd,'序列号']))
            wt = shutDownParaWorkTime(fileData,iStart,iEnd,yangT,timeThrehold ,speedThrehold)
            workTime = workTime + wt
            iStart = ind

    iEnd = pointNum - 1
    if debugFlag:
        print("\nindexDisContinuous : 2-iStart=%d,iEnd=%d" % (fileData.loc[iStart,'序列号'], fileData.loc[iEnd,'序列号']))
    wt = shutDownParaWorkTime(fileData, iStart, iEnd, yangT, timeThrehold, speedThrehold)
    workTime = workTime + wt
    return workTime


def batchWorkTimeWithoutStopTime(timeThrehold = 300,speedThrehold = 1):
    """
    除去 开机停歇、关机停歇 以及分时段处理一个地块的情况，剩下轨迹点的工作时间
    :return:
    """
    rootP = r'D:\mmm\实验数据\test21-总作业时长\开机停歇'
    test21Data = pda.read_excel(rootP + '/test21-轨迹索引-v2.0.xlsx')

    test21_result_info = pda.DataFrame(columns=['文件名称', '总工作时长','总工作时长秒'])

    for i in test21Data.index:

        fileName = test21Data.loc[i, '文件名称']
        yangT=test21Data.loc[i, '采样时间']
        print(fileName)
        fileData = pda.read_excel(r'D:/mmm/轨迹数据集/汇总/' + fileName)
        workTime = indexDisContinuous(fileData,yangT,timeThrehold,speedThrehold)
        test21_result_info.loc[i] = [fileName, str(workTime),workTime.total_seconds()]
        if i % 10 == 0:
            test21_result_info.to_excel(rootP + '/test21-总时间统计(除去开关机停歇时间)_1008.xlsx')

    test21_result_info.to_excel(rootP + '/test21-总时间统计(除去开关机停歇时间)_1008.xlsx')

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

# batchTotalTime()
# batchGetNoWorkTime()
# t1,t2,t3 =aFileNoWorkTime('00845 种-中-梭==皖01-00233_2020-6-12==0612-0705-filed.xlsx',2,['7257, 9169'])
# print(t1)
# print(t2)
# print(t3)

# 全局变量，用于控制 是否打印 中间变量信息   0-不打印   1-打印
global debugFlag
debugFlag = 1

# # aFileLongTimeNoWork('00023 耕-大-梭==黑02-S45271_2018-05-05==0504-2148-filed.xlsx')
# # batchLongTimeNoWork()
# fileData = pda.read_excel('D:/mmm/轨迹数据集/汇总/' + "00573 耕-中-绕==湘07-600001_2020-11-15==1115-0546-filed.xlsx")
# # wt = bootUpParaWorkTime(fileData,819,1631,4)
# #
# wt = indexDisContinuous(fileData,4,300,1)
# # # # wt = shutDownParaWorkTime(fileData,0,2687,2)
# print(wt)

batchWorkTimeWithoutStopTime()