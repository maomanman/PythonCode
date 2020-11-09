import pandas as pda
import numpy as npy
import math as ma
import time
import datetime
import os
# 这两个是用于的打开文件选择框
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# 这些是用来读写excel文件的
import xlwt
import xlrd
from xlutils.copy import copy

'''
2.0 版本相对 1.0 版本 更新的内容 :
1、用墨卡托坐标代替原来计算的XY坐标进行各种量的其他计算，plot画图所用的坐标还是 文献中简化后的 xy 坐标
2、标记了信号漂移点，并进行单独存储，结果文件中进行了删除处理
3、将文件进行了模块化处理

3.0 版本相对 2.0 版本 更新的 内容有：
1、将plot画图用的坐标换成 墨卡托坐标
'''


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


def CalDisByLoLangitude(lon1, lat1, lon2, lat2):
    """
    根据两点的经纬度计算两点直线距离
    :param lon1: 第一个点的 经度
    :param lat1: 第一个点的 纬度
    :param lon2: 第二个点的 经度
    :param lat2: 第二个点的 纬度
    :return:  两点的直线距离
    """
    distence = 0
    temp = ma.sin(lat1) * ma.sin(lat2) * ma.cos(lon1 - lon2) + ma.cos(lat1) * ma.cos(lat2)
    if temp > 1 or temp < -1:
        # print('i = {},temp = {}'.format(i,temp))
        if lon1 == lon2 and lat1 == lat2:
            distence = 0
    else:
        distence = 6371004 * ma.acos(temp) * ma.pi / 180.0
    return distence


def LoLatitudeChangeToXY(origin, lon, lat):
    """
    一个经纬度坐标 转换 成 指定参考系中的 XY 坐标
    :param origin:  原点，即参考经纬度
    :param lon:  需要装换的 经度
    :param lat:  需要装换的 纬度
    :return:  x y
    """
    return origin.ToX(lon), origin.ToY(lat)


def LoLatitudeChangeToXY_batch(b_lon, b_lat):
    """
    批量 经纬度坐标 转换 成 XY 坐标
    :param b_lon:  经度
    :param b_lat:  纬度
    :return:  x , y
    """
    col = len(b_lon)  # 数据长度
    origin = GetPoint(b_lon[0], b_lat[0])  # 置 第一个 经纬度 为参考点
    x = []
    y = []
    for i in range(1, col):
        x.append(origin.ToX(b_lon[i]))
        y.append(origin.ToY(b_lat[i]))
    return x, y


def LonLatitude2WebMercator(lon, lat):
    """
    将经纬度转换成墨卡托坐标
    :param lon: 经度
    :param lat:  纬度
    :return: 墨卡托坐标 X Y
    """
    earthRad = 6378137.0

    x = lon * npy.pi / 180 * earthRad
    a = lat * npy.pi / 180
    y = earthRad / 2 * npy.log((1.0 + npy.sin(a)) / (1.0 - npy.sin(a)))
    return x, y


def DisOnlineFromOnePointToAnother(lon1, lat1, angle1, lon2, lat2):
    """
    点2 到 点1 所在直线（直线斜率由 点1 平均航向角所得）的 最短距离
    :param lon1: 点1 经度
    :param lat1: 点1 纬度
    :param angle1: 点1 平均航向角
    :param lon2: 点2 经度
    :param lat2: 点2 纬度
    :return: 距离
    """
    origin = GetPoint(lon1, lat1)  # 将 点1 设置为原点
    x, y = LoLatitudeChangeToXY(origin, lon2, lat2)  # 换算 点2 的 XY 大地坐标

    # 求点2 的距离坐标
    dis = CalDisByLoLangitude(lon1, lat1, lon2, lat2)  # 计算 点1 到 点2 的直线距离 单位：米
    # 点2 到 点1 连线的斜率
    if x == 0:
        x_m = 0
        y_m = dis
    else:
        k = y / x
        ang_k = ma.atan(k)
        x_m = dis * ma.cos(ang_k)  # 单位 米
        y_m = dis * ma.sin(ang_k)

    # 求点1 所在线 的斜率
    if angle1 == 0 or angle1 == 360 and angle1 == 180:
        return ma.fabs(x)
    elif 0 < angle1 < 180:
        ag = (90 - angle1) * ma.pi / 180  # 倾斜角 弧度
    else:
        ag = (270 - angle1) * ma.pi / 180
    a = ma.tan(ag)  # 斜率

    # 直线方程 a X - Y = 0
    return ma.fabs(a * x_m - y_m) / ma.sqrt(a * a + 1)


def DisOnlineFromOnePointToAnotherByXY(lon1, lat1, angle1, lon2, lat2):
    """
    点2 到 点1 所在直线（直线斜率由 点1 平均航向角所得）的 最短距离
    :param lon1: 点1 经度
    :param lat1: 点1 纬度
    :param angle1: 点1 平均航向角
    :param lon2: 点2 经度
    :param lat2: 点2 纬度
    :return: 点到线的 最短距离
    """
    x1, y1 = LonLatitude2WebMercator(lon1, lat1)
    x2, y2 = LonLatitude2WebMercator(lon2, lat2)
    x = x2 - x1
    y = y2 - y1

    # 求点2 的距离坐标

    dis = CalDisByLoLangitude(lon1, lat1, lon2, lat2)  # 计算 点1 到 点2 的直线距离 单位：米
    # 点2 到 点1 连线的斜率
    if x == 0:
        x_m = 0
        if y > 0:
            y_m = dis
        else:
            y_m = -dis
    else:
        k = y / x
        ang_k = ma.atan(k)
        x_m = dis * ma.cos(ang_k)  # 单位 米
        y_m = dis * ma.sin(ang_k)

    # 求点1 所在线 的斜率
    if angle1 == 0 or angle1 == 360 and angle1 == 180:
        return ma.fabs(y_m)
    elif angle1 > 0 and angle1 < 180:
        ag = (90 - angle1) * ma.pi / 180  # 倾斜角 弧度
    else:
        ag = (270 - angle1) * ma.pi / 180
    a = ma.tan(ag)  # 斜率

    # 直线方程 a X - Y = 0
    return ma.fabs(a * x_m - y_m) / ma.sqrt(a * a + 1)


def GetSectionFileName(sourFileName, GpsTime, tpyeFlag=1):
    """
    获取切片文件名
    根据原文件名，和 切片文件第一个GPS时间，以及类型标志（1=地块、0=道路，默认是地块）拼写切片文件名
    :param sourFileName:  原文件名称
    :param GpsTime: 切片文件第一个轨迹点的GPS时间
    :param tpyeFlag: 类型标志:1-地块，0-道路
    :return: 切片文件名
    """

    monthAndDay = "{:02d}{:02d}".format(GpsTime.month, GpsTime.day)
    hourAndMinute = "{:02d}{:02d}".format(GpsTime.hour, GpsTime.minute)

    sf = sourFileName.split('.')

    if tpyeFlag == 1:
        sectionFileName = sf[0] + '==' + monthAndDay + '-' + hourAndMinute + '-field.' + sf[1]
    else:
        sectionFileName = sf[0] + '==' + monthAndDay + '-' + hourAndMinute + '-road.' + sf[1]

    return sectionFileName


def SplitfieldByMoreAtrributes(data, fileName):
    """
    联合多种属性分割地块
    :param data: 读取的excel文件数据
    :param fileName : excel 文件所在的路径及文件名
    :return: data 处理后的excel文件数据
             x    用于画图的横坐标
             y    用于画图的纵坐标
    """
    head_text = list(data.columns)  # 获取数据的 列标签
    # 取列标签下标
    # 标签名用字典表示
    dict = {'depth': 0, 'toolState': 0, 'longitude': 0, 'latitude': 0, 'angel': 0}

    for i, tag in enumerate(head_text):
        if tag.find('作业深度') != -1:
            dict['depth'] = head_text[i]
        elif tag.find('机具状态') != -1:
            dict['toolState'] = head_text[i]
        elif tag.find('经度') != -1:
            dict['longitude'] = head_text[i]
        elif tag.find('纬度') != -1:
            dict['latitude'] = head_text[i]
        elif tag.find('航向') != -1:
            dict['angel'] = head_text[i]
        elif tag.find('作业幅宽') != -1:
            workWidth = max(data[head_text[i]])
        elif tag.find('GPS时间') != -1:
            dict['GPStime'] = head_text[i]

    col = len(data.values)

    start = time.time()
    dict['timeDiff'] = '时间间隔'
    if dict['timeDiff'] not in data.columns:
        data[dict['timeDiff']] = 0  # 初始化
        data.loc[0, dict['timeDiff']] = 0
        for i in range(1, col):
            timeTemp = data.loc[i, dict['GPStime']] - data.loc[i - 1, dict['GPStime']]  # Timedelta('0 days 00:00:02')
            data.loc[i, dict['timeDiff']] = timeTemp.total_seconds()
    else:
        if type(data.loc[2, dict['timeDiff']]) == str:
            for i in range(1, col):
                timeTemp = data.loc[i, dict['timeDiff']].split(':')
                data.loc[i, dict['timeDiff']] = int(timeTemp[0]) * 3600 + int(timeTemp[1]) * 60 + int(timeTemp[2])
        elif type(data.loc[2, dict['timeDiff']]) == datetime.time:
            for i in range(1, col):
                timeTemp = data.loc[i, dict['timeDiff']]
                data.loc[i, dict['timeDiff']] = timeTemp.hour * 3600 + timeTemp.minute * 60 + timeTemp.second
        print('时间间隔  标签已存在')

    dict['countOfSameToolState'] = '相同机具状态个数'  # 将标签名添加到字典中
    if '相同机具状态个数' not in data.columns:  # 标签没有则新加入
        data[dict['countOfSameToolState']] = 1
        same_num = 1
        for i in range(1, col):
            # 当前 机具状态 与 前 一个 机具状态 相同  则 计数
            if data.loc[i][dict['toolState']] == data.loc[i - 1][dict['toolState']]:
                same_num += 1
                if i == col - 1:  # 若运行到最后一条数据 则直接进行登记
                    data.loc[i - same_num:i, dict['countOfSameToolState']] = same_num
            else:
                data.loc[i - same_num:i - 1, dict['countOfSameToolState']] = same_num
                same_num = 1
    else:
        print('相同机具状态个数 标签存在')

    # 计算 相邻点距离
    dict['distanceBetweenAdjacentPoints'] = '相邻点距离'
    dict['dirtyPoint'] = '野点'
    if '相邻点距离' not in data.columns:  # 标签没有则新加入
        data[dict['distanceBetweenAdjacentPoints']] = 0
        data[dict['dirtyPoint']] = 0
        # speedThreshold_field = 2.7778  # < 10km/h  ~ 2.77778 m/s  农机田间作业速度一般在 10 km /h 以内
        # speedThreshold_road = 8.3333  # <= 30km/h ~ 8.3333m/s   道路上行驶时最高时速不超过 30 km /h
        for i in range(1, col):  # 从第二条数据开始遍历
            dis = CalDisByLoLangitude(data.loc[i][dict['longitude']], data.loc[i][dict['latitude']], data.loc[i - 1][
                dict['longitude']], data.loc[i - 1][dict['latitude']])
            data.loc[i, dict['distanceBetweenAdjacentPoints']] = dis
            # if dis / data.loc[i, dict['timeDiff']] > (
            # speedThreshold_field if data.loc[i, dict['toolState']] == 1 else speedThreshold_road):
            #     if data.loc[i - 1, dict['dirtyPoint']] != 4:  # 前面一个点不是信号漂移点
            #         data.loc[i - 1, dict['dirtyPoint']] = 4  # 信号漂移点
            # elif data.loc[i - 1, dict['dirtyPoint']] == 4:  # 前面一个点是信号漂移点
            #     data.loc[i - 1, dict['dirtyPoint']] = 4  # 与信号漂移点是正常速度，那该点也是信号漂移点

    else:
        print('相邻点间隔 标签存在')

    # 计算每一点的速度
    dict['velocity'] = '点速度'
    if dict['velocity'] not in data.columns:  # 标签没有则加入新标签
        data[dict['velocity']] = 0  # 初始化为 0
        dis = npy.array(data.loc[1:col - 1, dict['distanceBetweenAdjacentPoints']])  # 相邻点间距离
        t = npy.array(data.loc[1:col - 1, dict['timeDiff']])  # 相邻点间的采样间隔
        v = dis / t  # 速度
        data.loc[1:col - 1, dict['velocity']] = v

        driftIndex = npy.array(
            [i for i, v in enumerate(data.loc[:, dict['velocity']] > 20) if
             v == True])  # 点速度超过阈值(20m/s，没有啥科学依据，纯属分析原数据设定)的点的索引号
        newDriftIndex = []
        # 超速点标记为 第4类野点
        drInNum = len(driftIndex)
        for i in range(drInNum):
            '''
            信号漂移点情况分类：
            1、当前索引号的点 在 轨迹上前一个点是正常点，则这个索引号的点是 信号漂移点
                1、1 当前信号漂移点 在 轨迹上下一个点是正常点，则轨迹上下一个点是信号漂移点  (需循环检测下一个点)
            2、当前索引号的点 在 轨迹上前一个点信号漂移点，则这个索引号的点是 正常点
            
            '''
            #  2、当前索引号的点 在 轨迹上前一个点信号漂移点，则这个索引号的点是 正常点
            if i != 0 and data.loc[driftIndex[i] - 1, dict['dirtyPoint']] == 4:
                # 重新计算点速度
                preIndex = driftIndex[i] - 1  # 轨迹上 前一个点的索引号
                continueNum = 0  # 信号漂移点的连续个数
                while data.loc[preIndex, dict['dirtyPoint']] == 4:
                    if preIndex > 0:
                        preIndex -= 1
                        continueNum += 1
                    else:
                        break

                lon1 = data.loc[preIndex, dict['longitude']]
                lat1 = data.loc[preIndex, dict['latitude']]
                lon2 = data.loc[driftIndex[i], dict['longitude']]
                lat2 = data.loc[driftIndex[i], dict['latitude']]
                dis = CalDisByLoLangitude(lon1, lat1, lon2, lat2)
                ti = ma.fsum(data.loc[preIndex + 1:driftIndex[i], dict['timeDiff']])
                data.loc[driftIndex[i], dict['velocity']] = dis / ti

                driftIndex[i] = 0
            else:  # 1、当前索引号的点 在 轨迹上前一个点是正常点，则这个索引号的点是 信号漂移点
                data.loc[driftIndex[i], dict['dirtyPoint']] = 4
                newDriftIndex.append(driftIndex[i])
                if i != drInNum - 1:
                    nextIndex = driftIndex[i] + 1
                    # 1、1 当前信号漂移点 在 轨迹上下一个点是正常点，则轨迹上下一个点是信号漂移点
                    while nextIndex != driftIndex[i + 1]:
                        if nextIndex < col:
                            data.loc[nextIndex, dict['dirtyPoint']] = 4
                            newDriftIndex.append(nextIndex)
                        nextIndex += 1

        if len(newDriftIndex):
            # 第四类野点数据进行另存为
            filePath = os.path.split(fileName)
            dirtyPointPath = filePath[0] + '/dirtyPoint'
            if not os.path.exists(dirtyPointPath):
                os.mkdir(dirtyPointPath)
            dirtyPointExeclName = dirtyPointPath + '/' + os.path.split(fileName)[1].split('.')[0] + '-dirtyPoint.xlsx'

            data.loc[newDriftIndex].set_index('序列号').to_excel(dirtyPointExeclName)

            # 删除第4类野点
            data.drop(newDriftIndex, inplace=True)
            data.reset_index(drop=True, inplace=True)
            col = len(data.values)
    else:
        print(dict['velocity'] + '标签存在')

    # 计算 调整后机具状态
    dict['adjustedToolState'] = '调整后机具状态'
    if '调整后机具状态' not in data.columns:  # 标签没有则新加入
        data[dict['adjustedToolState']] = 0
        toolContinum_threshold = 4  # 相同状态个数的 阈值
        # 调整后的机具状态 初始化 为原状态
        data.loc[:, dict['adjustedToolState']] = data.loc[:, dict['toolState']]

        i = 0
        while i < col:  # 循环遍历每一条数据，从第二条开始遍历
            # 机具状态可能存在 不为0  和 不为1 的情况
            if data.loc[i, dict['toolState']] != 1 and data.loc[i, dict['toolState']] != 0:
                data.loc[i:(i + data.loc[i, dict['countOfSameToolState']] - 1),
                dict['adjustedToolState']] = 0  # 其他状态都调整为 0
            # 当前状态连续个数小于等于阈值，视为野点，并进行状态调整
            if data.loc[i, dict['countOfSameToolState']] <= toolContinum_threshold:
                # 标记野点
                data.loc[i:(i + data.loc[i, dict['countOfSameToolState']] - 1), dict['dirtyPoint']] = 1
                # 调整状态 （调整为同上一个状态）
                data.loc[i:(i + data.loc[i, dict['countOfSameToolState']] - 1), dict['adjustedToolState']] = data.loc[
                    i - 1, dict['adjustedToolState']]
            # 下标跳转 野点个数 长度
            i += data.loc[i, dict['countOfSameToolState']]
    else:
        print('调整后机具状态 标签存在')

    cotinuePointThreshold = 10  # 连续作业 的 轨迹点  少于 10 标记为野点3  且不能判断 为 地块

    # 计算 调整后相同机具状态个数
    dict['countOfAdjustedSameToolState'] = '调整后相同机具状态个数'
    if '调整后相同机具状态个数' not in data.columns:  # 标签没有则新加入

        data['调整后相同机具状态个数'] = 1
        same_num = 1
        for i in range(1, col):  # 从第二条数据开始遍历
            # 当前 机具状态 同 前一条数据 机具状态 相同 ，则进行 计数
            if data.loc[i][dict['adjustedToolState']] == data.loc[i - 1][dict['adjustedToolState']]:
                same_num += 1
                if i == col - 1:  # 遍历到最后一条数据 则直接登记
                    data.loc[(i - same_num):i, dict['countOfAdjustedSameToolState']] = same_num
                    if data.loc[i][
                        dict['adjustedToolState']] == 1 and same_num < cotinuePointThreshold:  # 连续作业的轨迹点少于 10 个 判断为野点 3
                        data.loc[(i - same_num):i, dict['dirtyPoint']] = 3
            else:  # 否则，相同状态计数结束，并进行登记
                if data.loc[i - 1][
                    dict['adjustedToolState']] == 1 and same_num < cotinuePointThreshold:  # 连续作业的轨迹点少于 10 个 判断为野点 3
                    data.loc[(i - same_num):i - 1, dict['dirtyPoint']] = 3  # 标记为野点，虽是工作点，但是跟着前后空行进行计数
                    same_num = data.loc[i - same_num - 1, dict['countOfAdjustedSameToolState']] + same_num + 1
                else:
                    data.loc[(i - same_num):(i - 1), dict['countOfAdjustedSameToolState']] = same_num
                    same_num = 1  # 下一个状态重新开始计数

    else:
        print('相同机具状态的平均航向角 标签存在')

    # 初步计算相同机具状态的平均航向角
    dict['averageAngleOfSameToolState'] = '相同机具状态的平均航向角'
    if '相同机具状态的平均航向角' not in data.columns:  # 标签没有则新加入

        data[dict['averageAngleOfSameToolState']] = 0
        i = 0
        while i < col:
            if data.loc[i, dict['adjustedToolState']] == 1:  # 工作行 才 计算 平均航向角
                sameNum = data.loc[i, dict['countOfAdjustedSameToolState']]
                if sameNum > 4:  # 工作航轨迹点个数 大于 4 个 才考虑工作行的起止点对平均航向角的影响
                    sameNum = sameNum - 4
                    step = 2
                    startPoint = i + step
                    endPoint = i + sameNum - 1 + step
                else:
                    step = 0
                    startPoint = i + step
                    endPoint = i + sameNum - 1
                temp = ma.fsum(data.loc[startPoint:endPoint, dict['angel']]) / sameNum
                maxAngle = max(data.loc[startPoint:endPoint, dict['angel']])
                minAngle = min(data.loc[startPoint:endPoint, dict['angel']])
                if maxAngle > 345 and minAngle < 15:  # 航向角在 360 左右 的进行修正
                    lowNum = sum(data.loc[startPoint:endPoint, dict['angel']] < 15)
                    upNum = sum(data.loc[startPoint:endPoint, dict['angel']] > 345)
                    if lowNum < upNum:  # 小于15的更少则将其修正为300+
                        temp = (ma.fsum(data.loc[startPoint:endPoint, dict['angel']]) + lowNum * 360) / sameNum
                    else:  # 大于345度的更少，则将其修为0+
                        upIndex = list(
                            npy.array([j for j, x in enumerate(data.loc[startPoint:endPoint, dict['angel']] > 345) if
                                       x == True]) + i + step)  # 航向角大于300 的索引号
                        upSum = sum(data.loc[startPoint:endPoint, dict['angel']][upIndex])  # 航向角大于 300的 所有航向角之和
                        temp = (360 * upNum - upSum + sum(
                            data.loc[startPoint:endPoint, dict['angel']]) - upSum) / sameNum
                    # if lowNum <= sameNum / 2:  # 少于 一半 的航向角 是在 10 度 以内的
                    #     temp = (ma.fsum(data.loc[startPoint:endPoint, dict['angel']]) + lowNum * 360) / sameNum
                    # else:  # 少于 一半 的航向角 是在 300 度 以上
                    #     upNum = sum(data.loc[startPoint:endPoint, dict['angel']] > 300)
                    #     upIndex = list(
                    #         npy.array([j for j, x in enumerate(data.loc[startPoint:endPoint, dict['angel']] > 300) if
                    #                    x == True]) + i + step)  # 航向角大于300 的索引号
                    #     upSum = sum(data.loc[startPoint:endPoint, dict['angel']][upIndex])  # 航向角大于 300的 所有航向角之和
                    #     temp = (360 * upNum - upSum + sum(
                    #         data.loc[startPoint:endPoint, dict['angel']]) - upSum) / sameNum

                data.loc[i:(i + data.loc[i, dict['countOfAdjustedSameToolState']] - 1),
                dict['averageAngleOfSameToolState']] = temp
                i += data.loc[i, dict['countOfAdjustedSameToolState']]
            else:
                i += data.loc[i, dict['countOfAdjustedSameToolState']]
    else:
        print('调整后相同机具状态个数 标签存在')

    # 计算 每一次同机具状态连续行驶的首尾直线距离
    dict['distanceOfOneState'] = '每一次同机具状态连续行驶的首尾直线距离'
    if dict['distanceOfOneState'] not in data.columns:
        data[dict['distanceOfOneState']] = 0
        i = 0
        while i < col:
            count = data.loc[i, dict['countOfAdjustedSameToolState']]  # 连续状态个数
            # 根据首尾点 的 经纬度计算 直线距离
            dis = CalDisByLoLangitude(data.loc[i][dict['longitude']], data.loc[i][dict['latitude']],
                                      data.loc[i + count - 1][dict['longitude']],
                                      data.loc[i + count - 1][dict['latitude']])
            data.loc[i:i + count - 1, dict['distanceOfOneState']] = dis
            i += count
    else:
        print('每一次同机具状态连续行驶的首尾直线距离 标签已存在')

    # 计算 点2 到 点1 所在直线的距离
    dict['disOfPointLine'] = '空行时点2到点1所在直线的距离'
    if dict['disOfPointLine'] not in data.columns:
        data[dict['disOfPointLine']] = 0  # 初始化为 0
        i = 0
        while i < col:
            if data.loc[i, dict['adjustedToolState']] == 0:  # 判断空行
                spacePoint = data.loc[i, dict['countOfAdjustedSameToolState']]
                if i == 0:
                    lon1 = data.loc[i, dict['longitude']]
                    lat1 = data.loc[i, dict['latitude']]
                    angle1 = data.loc[i, dict['angel']]
                else:
                    lon1 = data.loc[i - 1, dict['longitude']]
                    lat1 = data.loc[i - 1, dict['latitude']]
                    angle1 = data.loc[i - 1, dict['averageAngleOfSameToolState']]
                lon2 = data.loc[i + spacePoint - 1, dict['longitude']]
                lat2 = data.loc[i + spacePoint - 1, dict['latitude']]
                # dis = DisOnlineFromOnePointToAnother(lon1, lat1, angle1, lon2, lat2)
                dis = DisOnlineFromOnePointToAnotherByXY(lon1, lat1, angle1, lon2, lat2)
                data.loc[i:i + spacePoint - 1, dict['disOfPointLine']] = dis
                i += spacePoint
            else:  # 工作行不计算
                i += data.loc[i, dict['countOfAdjustedSameToolState']]
    else:
        print('点2到点1所在直线的距离 标签已存在')

    # 计算相邻 工作行（机具状态 = 1） 的航向角之差
    dict['angelDiffOfSameToolState'] = '相邻工作行的航向角之差'
    if '相邻工作行的航向角之差' not in data.columns:
        data[dict['angelDiffOfSameToolState']] = 0  # 初始化
        i = 0
        while i < col:
            if data.loc[i, dict['adjustedToolState']] == 1:  # 判断是否是工作行
                ag1 = data.loc[i, dict['averageAngleOfSameToolState']]  # 第一个工作行的平均航向角
                workPoint1 = data.loc[i, dict['countOfAdjustedSameToolState']]  # 第一个工作行的点个数
                if i + workPoint1 < col:  # 如果是最后一行工作行
                    spacePoint = data.loc[i + workPoint1, dict['countOfAdjustedSameToolState']]  # 间隔空行的 点个数
                    if i + workPoint1 + spacePoint < col:  # 如果是最后一行 空行行
                        ag2 = data.loc[i + workPoint1 + spacePoint, dict['averageAngleOfSameToolState']]  # 第二个工作行的平均航向角
                        agDiff = ma.fabs(ag2 - ag1)
                        if agDiff > 180:
                            agDiff = 360 - agDiff  # 调整为最小角度差
                        workPoint2 = data.loc[
                            i + workPoint1 + spacePoint, dict['countOfAdjustedSameToolState']]  # 第一个工作行的点个数
                        data.loc[i:i + workPoint1 - 1, dict['angelDiffOfSameToolState']] = agDiff  # 登记 航向角之差
                        data.loc[i + workPoint1 + spacePoint:i + workPoint1 + spacePoint + workPoint2 - 1,
                        dict['angelDiffOfSameToolState']] = agDiff  # 登记 航向角之差
                        # 根据 航向角 筛选 野点，野点标注 为 2
                        # 航向角之差在 30 度 之内 视中间的空闲行驶点为野点 (判断点到直线的距离是为了规避 两个地块的作业方位一样但地块间有距离)
                        if ma.fabs(ag2 - ag1) <= 30 and \
                                (data.loc[i + workPoint1, dict['disOfPointLine']] <= 3 * workWidth or \
                                 data.loc[i + workPoint1, dict['distanceOfOneState']] <= 3 * workWidth):
                            data.loc[i + workPoint1:i + workPoint1 + spacePoint - 1, dict['dirtyPoint']] = 2
                        i = i + workPoint1 + spacePoint
                    else:
                        break
                else:
                    break
            else:  # 如果 不是工作行，则跳过
                i = i + data.loc[i, dict['countOfAdjustedSameToolState']]

    # 判断 地块
    dict['field'] = '地块标志'
    if dict['field'] not in data.columns:
        # data[dict['field']] = data[dict['adjustedToolState']]
        data[dict['field']] = 0  # 初始化为 0
        i = 0
        rownum = 0
        flag = 1

        while i < col:
            if data.loc[i, dict['adjustedToolState']] == 1 and (
                    data.loc[i, dict['angelDiffOfSameToolState']] <= 30 or
                    data.loc[i, dict['angelDiffOfSameToolState']] >= 160 or
                    (data.loc[i, dict['angelDiffOfSameToolState']] >= 65 and
                     data.loc[i, dict['angelDiffOfSameToolState']] <= 115)):
                workPoint1 = data.loc[i, dict['countOfAdjustedSameToolState']]  # 连续工作行的点个数
                if i + workPoint1 < col:  # 工作行 + 空行 +工作行/结束
                    spacePoint = data.loc[i + workPoint1, dict['countOfAdjustedSameToolState']]
                    # 判断 空行 首尾点的直线距离 与 幅宽 的关系  ：直线距离  <= 2 * 幅宽 --> 空行属于当前行所在地块
                    # if data.loc[i + workPoint1, dict['distanceOfOneState']] <= 3 * workWidth or \
                    # 判断 空行与相邻工作行的首尾点所在直线距离 与 幅宽 的关系  ：直线距离  <= 3 * 幅宽 --> 空行属于当前行所在地块
                    if data.loc[i + workPoint1, dict['disOfPointLine']] <= 3 * workWidth or \
                            data.loc[i + workPoint1, dict['dirtyPoint']] != 0:  # 空行 标志为 野点，也属于当前所在地块
                        if i + workPoint1 + spacePoint < col:  # 工作行 + 空行 +工作行 ....
                            # workPoint2 = data.loc[i + workPoint1 + spacePoint, dict['countOfAdjustedSameToolState']]
                            rownum += workPoint1 + spacePoint
                            i = i + workPoint1 + spacePoint
                        else:  # 工作行 + 空行 + 结束  # 退出循环
                            rownum += workPoint1  # 当前工作行属于上一块地，下一空行不属于 地块
                            i += workPoint1
                            # if rownum > cotinuePointThreshold:  # 连续作业 的 轨迹点  少于 10 不能判断 为 地块
                            data.loc[i - rownum, dict['field']] = rownum
                            data.loc[i - rownum + 1:i - 1, dict['field']] = flag  # 地块标志为 非0
                            flag += 1
                    else:  # 空行不属于当前行所在地块
                        rownum += workPoint1  # 当前工作行属于上一块地，下一空行不属于 地块
                        i += workPoint1
                else:  # 工作行 + 结束  # 退出循环
                    rownum += workPoint1  # 当前工作行属于上一块地
                    i += workPoint1
                    # if rownum > cotinuePointThreshold:  # 连续作业 的 轨迹点  少于 10 不能判断 为 地块
                    data.loc[i - rownum, dict['field']] = rownum
                    data.loc[i - rownum + 1:i - 1, dict['field']] = flag  # 地块标志为 非0
                    flag += 1
            elif data.loc[i, dict['adjustedToolState']] == 1:  # 当前工作行属于上一工作行所在地块，但与下一工作行不属于一块地
                workPoint2 = data.loc[i, dict['countOfAdjustedSameToolState']]
                rownum += workPoint2
                i += workPoint2
                #  if rownum > cotinuePointThreshold:  # 连续作业 的 轨迹点  少于 10 不能判断 为 地块
                data.loc[i - rownum, dict['field']] = rownum
                data.loc[i - rownum + 1:i - 1, dict['field']] = flag  # 地块标志为 非0
                flag += 1
                rownum = 0
            else:  # 非工作行
                if rownum > 0:
                    data.loc[i - rownum, dict['field']] = rownum
                    data.loc[i - rownum + 1:i - 1, dict['field']] = flag  # 地块标志为非0
                    flag += 1
                    rownum = 0
                spacePoint = data.loc[i, dict['countOfAdjustedSameToolState']]
                i += spacePoint
    else:
        print('地块标志 标签已存在')

    # 批量转换成 坐标
    x = []
    y = []
    i = 0
    while i < col:
        if data.loc[i, dict['field']] != 0:  # 地块标志 都不等于 0
            fieldNum = data.loc[i, dict['field']]

            # region 将经纬度批量转换成简化 XY 坐标
            # b_lon = list(data.loc[i:i + fieldNum - 1, dict['longitude']])
            # b_lat = list(data.loc[i:i + fieldNum - 1, dict['latitude']])
            # x_b, y_b = LoLatitudeChangeToXY_batch(b_lon, b_lat)
            # endregion
            # region 将经纬度批量转换成 墨卡托 坐标
            x_b = list(data.loc[i:i + fieldNum - 1, 'x'])
            y_b = list(data.loc[i:i + fieldNum - 1, 'y'])
            # endregion

            x.extend(x_b)
            y.extend(y_b)
            x.append('a')
            y.append('a')
            i += fieldNum
        else:
            i += data.loc[i, dict['countOfAdjustedSameToolState']]

    # region 用于画出地块边框所需标签
    # 将野点忽略，标记完整的作业行
    dict['lenthOfWorkLine'] = '完整作业行的首尾距离'
    dict['countOfWorkLine'] = '完整作业行的轨迹点个数'
    dict['rowIndexOffield'] = '一块地的完整作业行行数'
    if dict['lenthOfWorkLine'] not in data.columns:
        data[dict['lenthOfWorkLine']] = 0
        data[dict['countOfWorkLine']] = 0
        data[dict['rowIndexOffield']] = 0
        i = 0
        while i < col:
            if data.loc[i, dict['field']] != 0:
                pointCountOffield = data.loc[i, dict['field']]  # 一块地的轨迹点总数
                j = 0
                rownum = 0
                fieldRowIndex = 1
                while j < pointCountOffield:
                    if data.loc[i + j, dict['adjustedToolState']] == 1:
                        rownum += data.loc[i + j, dict['countOfAdjustedSameToolState']]
                    elif data.loc[i + j, dict['dirtyPoint']] != 0:
                        rownum += data.loc[i + j, dict['countOfAdjustedSameToolState']]
                    else:
                        # 是一行的轨迹点 则统计该行轨迹点总数 和 计算首尾直线距离
                        lon1 = data.loc[i + j - rownum, dict['longitude']]
                        lat1 = data.loc[i + j - rownum, dict['latitude']]
                        lon2 = data.loc[i + j - 1, dict['longitude']]
                        lat2 = data.loc[i + j - 1, dict['latitude']]
                        dis = CalDisByLoLangitude(lon1, lat1, lon2, lat2)
                        data.loc[i + j - rownum:i + j - 1, dict['lenthOfWorkLine']] = dis
                        data.loc[i + j - rownum:i + j - 1, dict['countOfWorkLine']] = rownum
                        data.loc[i + j - rownum:i + j - 1, dict['rowIndexOffield']] = fieldRowIndex
                        rownum = 0
                        fieldRowIndex += 1

                    j += data.loc[i + j, dict['countOfAdjustedSameToolState']]
                else:  # 一块地以最后一行作业行结束，结束后计算并登记该块地的信息
                    lon1 = data.loc[i + j - rownum, dict['longitude']]
                    lat1 = data.loc[i + j - rownum, dict['latitude']]
                    lon2 = data.loc[i + j - 1, dict['longitude']]
                    lat2 = data.loc[i + j - 1, dict['latitude']]
                    dis = CalDisByLoLangitude(lon1, lat1, lon2, lat2)
                    data.loc[i + j - rownum:i + j - 1, dict['lenthOfWorkLine']] = dis
                    data.loc[i + j - rownum:i + j - 1, dict['countOfWorkLine']] = rownum
                    data.loc[i + j - rownum:i + j - 1, dict['rowIndexOffield']] = fieldRowIndex
                i += pointCountOffield
            else:
                i += data.loc[i, dict['countOfAdjustedSameToolState']]
    else:
        print(dict['lenthOfWorkLine'] + ' 标签已存在')

    # 分割出地块外形边框的轨迹点  并按地块将文件进行切割
    # i = 0
    shape_x = []
    shape_y = []
    # while i < col:
    #     if data.loc[i, dict['field']] != 0:
    #         # 是地块
    #         step = data.loc[i, dict['field']]
    #         # sectionFileName = GetSectionFileName(fileName,data.loc[i,dict['GPStime']])
    #         j = 0
    #         rownum = 0
    #         while j < step:
    #
    #             if data.loc[i + j, dict['rowIndexOffield']] != 0:
    #                 rownum = data.loc[i + j, dict['countOfWorkLine']]
    #
    #                 if j == 0:
    #                     ag1 = data.loc[i + j, dict['averageAngleOfSameToolState']]
    #                     startPoint = {'x': data.loc[i + j, 'x'], 'y': data.loc[i + j, 'y']}
    #                     endPoint = {'x': data.loc[i + j + rownum - 1, 'x'], 'y': data.loc[i + j + rownum - 1, 'y']}
    #                     lines = [{'startPoint': startPoint, 'endPoint': endPoint}]  # 作业行的起止点坐标列表
    #                 else:
    #                     ag2 = data.loc[i + j, dict['averageAngleOfSameToolState']]
    #                     if ma.fabs(ag2 - ag1) < 30:  # 与第一行同向
    #                         startPoint = {'x': data.loc[i + j, 'x'], 'y': data.loc[i + j, 'y']}
    #                         endPoint = {'x': data.loc[i + j + rownum - 1, 'x'], 'y': data.loc[i + j + rownum - 1, 'y']}
    #                     # elif 65 < ma.fabs(ag2 - ag1) < 115: # 与第一行垂直  {还需要仔细分析}
    #                     #     startPoint = {'x': data.loc[i + j, 'x'], 'y': data.loc[i + j, 'y']}
    #                     #     endPoint = {'x': data.loc[i + j + rownum - 1, 'x'], 'y': data.loc[i + j + rownum - 1, 'y']}
    #                     else:  # 与第一行反向
    #                         endPoint = {'x': data.loc[i + j, 'x'], 'y': data.loc[i + j, 'y']}
    #                         startPoint = {'x': data.loc[i + j + rownum - 1, 'x'],
    #                                       'y': data.loc[i + j + rownum - 1, 'y']}
    #
    #                 lines.append({'startPoint': startPoint, 'endPoint': endPoint})
    #                 j += rownum
    #             else:
    #                 j += data.loc[i + j, dict['countOfAdjustedSameToolState']]  # 换行的转弯行使
    #         else:
    #             for li in range(len(lines)):
    #                 if li == 0:
    #                     # 第一行作业行起始点 x y 坐标
    #                     shape_x.append(lines[li]['startPoint']['x'])
    #                     shape_y.append(lines[li]['startPoint']['y'])
    #                     # 第一行作业行结束点 x y 坐标
    #                     shape_x.append(lines[li]['endPoint']['x'])
    #                     shape_y.append(lines[li]['endPoint']['y'])
    #                 else:
    #                     shape_x.append(lines[li]['endPoint']['x'])
    #                     shape_y.append(lines[li]['endPoint']['y'])
    #             lines.reverse()  # 反转作业行顺序
    #             for li in range(len(lines)):
    #                 shape_x.append(lines[li]['startPoint']['x'])
    #                 shape_y.append(lines[li]['startPoint']['y'])
    #
    #             shape_x.append('a')
    #             shape_y.append('a')
    #     else:
    #         # 是道路
    #         step = data.loc[i, dict['countOfAdjustedSameToolState']]
    #     i += step
    # # endregion

    end = time.time()
    print('运行时长 {} 秒'.format(end - start))
    return data, x, y, shape_x, shape_y


def RegisterForNewSectionFile(regFileName, values):
    """
    将切片的文件信息进行登记记录
    :param regFileName:  登记册文件名
    :param values: 需要登记的文件信息
    :return:
    """
    readFile = xlrd.open_workbook(regFileName, formatting_info=True)

    writeData = copy(readFile)
    writeSave = writeData.get_sheet(0)
    oldRowNum = readFile.sheet_by_index(0).nrows  # 获取表格中已存在的数据的行数
    for i in range(len(values)):
        writeSave.write(oldRowNum + i, 3, values[i][0])
        for j in range(1, len(values[i])):
            writeSave.write(oldRowNum + i, 7 + j, values[i][j])

    writeData.save(regFileName)


def SliptFile2SectionPart(data, fileName):
    """
    将原始文件数据进行切割，并保存为单个的excel文件，并登记记录相关信息
    :param data: 原始文件数据
    :return:
    """

    filePath = os.path.split(fileName)
    splitPointPath = filePath[0] + '/' + filePath[1].split('.')[0] + '-section'
    if not os.path.exists(splitPointPath):
        os.mkdir(splitPointPath)
    splitPointExeclName = splitPointPath + '/' + filePath[1]

    columns_array = data.columns.array  # 列标签名
    col = data.shape[0]
    i = 0
    registerInfo = []
    while i < col:
        if data.loc[i, '地块标志'] != 0:
            value = ['地块']
            step = int(data.loc[i, '地块标志'])
            countOfWorkPoint = int(sum(data.loc[i:i + step - 1, columns_array[3]] == 1))  # 原始所有机具状态为1 的 点总数
            sectionFileName = GetSectionFileName(splitPointExeclName, data.loc[i, 'GPS时间'])
            countOfValidPoint = int(sum(data.loc[i:i + step - 1, columns_array[2]] >= data.loc[i:i + step - 1,
                                                                                      columns_array[
                                                                                          10]]))  # 作业深度 >= 标准深度
            rowNum = int(data.loc[i:i + step - 1, '一块地的完整作业行行数'].max())
            # samplingTime = data.loc[i:i+step-1,'时间间隔'].mode()  # 时间间隔的 众数
            # totalTime = data.loc[i+step-1,'GPS时间']-data.loc[i,'GPS时间']
            # sectionFileNameOfNOTpath = os.path.split(sectionFileName)[1]

        else:
            value = ['道路']
            step = int(data.loc[i, '调整后相同机具状态个数'])
            sectionFileName = GetSectionFileName(splitPointExeclName, data.loc[i, 'GPS时间'], 0)
            countOfWorkPoint = 0
            countOfValidPoint = 0
            rowNum = 0

        samplingTime = int(data.loc[i:i + step - 1, '时间间隔'].mode()[0])  # 时间间隔的 众数
        strTime = str(data.loc[i + step - 1, 'GPS时间'] - data.loc[i, 'GPS时间']).split(' days ')
        strDay = strTime[1].split(':')
        strDay[0] = str(24 * int(strTime[0]) + int(strDay[0]))
        totalTime = ':'.join(strDay)
        sectionFileNameOfNOTpath = os.path.split(sectionFileName)[1]
        value.extend([step, countOfWorkPoint, countOfValidPoint, rowNum, samplingTime, str(data.loc[i, 'GPS时间']),
                      str(data.loc[i + step - 1, 'GPS时间']), totalTime, sectionFileNameOfNOTpath])
        registerInfo.append(value)
        data.loc[i:i + step - 1].set_index('序列号').to_excel(sectionFileName)
        i += step

    # regFileName = 'D:/mmm/python/轨迹测试数据/0927-将文件进行分割成多个文件/轨迹索引.xls'
     # RegisterForNewSectionFile(regFileName, registerInfo)


if __name__ == '__main__':
    window = Tk()
    window.withdraw()
    fileName = askopenfilename(title='打开文件', filetypes=[('All File', '*')])
    del window

    # 读excel数据
    data = pda.read_excel(fileName)
    # 处理excel数据
    data, x, y, shape_x, shape_y = SplitfieldByMoreAtrributes(data, fileName)

    # 切割文件 并进行登记
    SliptFile2SectionPart(data, fileName)

    data.set_index('序列号', inplace=True)

    # 保存文件
    timeStamp = datetime.datetime.now().strftime('%m%d-%H%M%S')
    f = fileName.split('.')
    # path_name = f[0]+'='+timeStamp+'.'+f[1]
    path_name_exl = f[0] + '-' + timeStamp + '.' + f[1]
    data.to_excel(path_name_exl)
    path_name_csv = f[0] + '-' + timeStamp + '.csv'
    data.to_csv(path_name_csv)
    # 删除变量
    del data
