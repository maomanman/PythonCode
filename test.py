import pandas as pda
import numpy as npy
import math as ma
import time
import datetime
# 这两个是用于的打开文件选择框
from tkinter import Tk
from tkinter.filedialog import askopenfilename


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
    elif angle1 > 0 and angle1 < 180:
        ag = (90 - angle1) * ma.pi / 180  # 倾斜角 弧度
    else:
        ag = (270 - angle1) * ma.pi / 180
    a = ma.tan(ag)  # 斜率

    # 直线方程 a X - Y = 0
    return ma.fabs(a * x_m - y_m) / ma.sqrt(a * a + 1)


window = Tk()
window.withdraw()
file_name = askopenfilename(title='打开文件', filetypes=[('All File', '*')])

del window

# 读excel数据
data = pda.read_excel(file_name)

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
        dict['workWidth'] = head_text[i]
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
    # speedThreshold_filed = 2.7778  # < 10km/h  ~ 2.77778 m/s  农机田间作业速度一般在 10 km /h 以内
    # speedThreshold_road = 8.3333  # <= 30km/h ~ 8.3333m/s   道路上行驶时最高时速不超过 30 km /h
    for i in range(1, col):  # 从第二条数据开始遍历
        dis = CalDisByLoLangitude(data.loc[i][dict['longitude']], data.loc[i][dict['latitude']], data.loc[i - 1][
            dict['longitude']], data.loc[i - 1][dict['latitude']])
        data.loc[i, dict['distanceBetweenAdjacentPoints']] = dis
        # if dis / data.loc[i, dict['timeDiff']] > (
        # speedThreshold_filed if data.loc[i, dict['toolState']] == 1 else speedThreshold_road):
        #     if data.loc[i - 1, dict['dirtyPoint']] != 4:  # 前面一个点不是信号漂移点
        #         data.loc[i - 1, dict['dirtyPoint']] = 4  # 信号漂移点
        # elif data.loc[i - 1, dict['dirtyPoint']] == 4:  # 前面一个点是信号漂移点
        #     data.loc[i - 1, dict['dirtyPoint']] = 4  # 与信号漂移点是正常速度，那该点也是信号漂移点

else:
    print('相邻点间隔 标签存在')

# 计算 调整后机具状态
dict['adjustedToolState'] = '调整后机具状态'
if '调整后机具状态' not in data.columns:  # 标签没有则新加入
    data[dict['adjustedToolState']] = 0
    toolContinum_threshold = 4  # 相同状态个数的 阈值
    num = 1
    # 调整后的机具状态 初始化 为原状态
    data.loc[:, dict['adjustedToolState']] = data.loc[:, dict['toolState']]

    i = 0
    while i < col:  # 循环遍历每一条数据，从第二条开始遍历
        # 当前状态连续个数小于等于阈值，视为野点，并进行状态调整
        if data.loc[i, dict['countOfSameToolState']] <= toolContinum_threshold:
            # 标记野点
            data.loc[i:(i + data.loc[i, dict['countOfSameToolState']] - 1), dict['dirtyPoint']] = 1
            # 调整状态 （调整为同上一个状态）
            data.loc[i:(i + data.loc[i, dict['countOfSameToolState']] - 1), dict['adjustedToolState']] = data.loc[
                i - 1, dict['adjustedToolState']]
            # 下标跳转 野点个数 长度
        if data.loc[i, dict['toolState']] != 1 and data.loc[i, dict['toolState']] != 0:  # 机具状态可能存在 不为0  和 不为1 的情况
            data.loc[i:(i + data.loc[i, dict['countOfSameToolState']] - 1), dict['adjustedToolState']] = 0
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
            if maxAngle > 300 and minAngle < 15:  # 航向角在 360 左右 的进行修正
                lowNum = sum(data.loc[startPoint:endPoint, dict['angel']] < 10)
                if lowNum <= sameNum / 2:  # 少于 一半 的航向角 是在 10 度 以内的
                    temp = (ma.fsum(data.loc[startPoint:endPoint, dict['angel']]) + lowNum * 360) / sameNum
                else:  # 少于 一半 的航向角 是在 300 度 以上
                    upNum = sum(data.loc[startPoint:endPoint, dict['angel']] > 300)
                    upIndex = list(
                        npy.array([j for j, x in enumerate(data.loc[startPoint:endPoint, dict['angel']] > 300) if
                                   x == True]) + i + step)  # 航向角大于300 的索引号
                    upSum = sum(data.loc[startPoint:endPoint, dict['angel']][upIndex])  # 航向角大于 300的 所有航向角之和
                    temp = (360 * upNum - upSum + sum(data.loc[startPoint:endPoint, dict['angel']]) - upSum) / sameNum

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
                                  data.loc[i + count - 1][dict['longitude']], data.loc[i + count - 1][dict['latitude']])
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
            dis = DisOnlineFromOnePointToAnother(lon1, lat1, angle1, lon2, lat2)
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
                            (data.loc[i + workPoint1, dict['disOfPointLine']] <= 3 * data.loc[i, dict['workWidth']] or \
                             data.loc[i + workPoint1, dict['distanceOfOneState']] <= 3 * data.loc[
                                 i, dict['workWidth']]):
                        data.loc[i + workPoint1:i + workPoint1 + spacePoint - 1, dict['dirtyPoint']] = 2
                    i = i + workPoint1 + spacePoint
                else:
                    break
            else:
                break
        else:  # 如果 不是工作行，则跳过
            i = i + data.loc[i, dict['countOfAdjustedSameToolState']]

# 判断 地块
dict['filed'] = '地块标志'
if dict['filed'] not in data.columns:
    # data[dict['filed']] = data[dict['adjustedToolState']]
    data[dict['filed']] = 0  # 初始化为 0
    i = 0
    rownum = 0
    flag = 1

    while i < col:
        if data.loc[i, dict['adjustedToolState']] == 1 and ( \
                        data.loc[i, dict['angelDiffOfSameToolState']] <= 30 or \
                        data.loc[i, dict['angelDiffOfSameToolState']] >= 160 or \
                        (data.loc[i, dict['angelDiffOfSameToolState']] >= 65 and \
                         data.loc[i, dict['angelDiffOfSameToolState']] <= 115)):
            workPoint1 = data.loc[i, dict['countOfAdjustedSameToolState']]  # 连续工作行的点个数
            if i + workPoint1 < col:  # 工作行 + 空行 +工作行/结束
                spacePoint = data.loc[i + workPoint1, dict['countOfAdjustedSameToolState']]
                # 判断 空行 首尾点的直线距离 与 幅宽 的关系  ：直线距离  <= 2 * 幅宽 --> 空行属于当前行所在地块
                # if data.loc[i + workPoint1, dict['distanceOfOneState']] <= 3 * data.loc[i, dict['workWidth']] or \
                # 判断 空行与相邻工作行的首尾点所在直线距离 与 幅宽 的关系  ：直线距离  <= 3 * 幅宽 --> 空行属于当前行所在地块
                if data.loc[i + workPoint1, dict['disOfPointLine']] <= 3 * data.loc[i, dict['workWidth']] or \
                        data.loc[i + workPoint1, dict['dirtyPoint']] != 0:  # 空行 标志为 野点，也属于当前所在地块
                    if i + workPoint1 + spacePoint < col:  # 工作行 + 空行 +工作行 ....
                        # workPoint2 = data.loc[i + workPoint1 + spacePoint, dict['countOfAdjustedSameToolState']]
                        rownum += workPoint1 + spacePoint
                        i = i + workPoint1 + spacePoint
                    else:  # 工作行 + 空行 + 结束  # 退出循环
                        rownum += workPoint1  # 当前工作行属于上一块地，下一空行不属于 地块
                        i += workPoint1
                        # if rownum > cotinuePointThreshold:  # 连续作业 的 轨迹点  少于 10 不能判断 为 地块
                        data.loc[i - rownum, dict['filed']] = rownum
                        data.loc[i - rownum + 1:i - 1, dict['filed']] = flag  # 地块标志为 非0
                        flag += 1
                else:  # 空行不属于当前行所在地块
                    rownum += workPoint1  # 当前工作行属于上一块地，下一空行不属于 地块
                    i += workPoint1
            else:  # 工作行 + 结束  # 退出循环
                rownum += workPoint1  # 当前工作行属于上一块地
                i += workPoint1
                # if rownum > cotinuePointThreshold:  # 连续作业 的 轨迹点  少于 10 不能判断 为 地块
                data.loc[i - rownum, dict['filed']] = rownum
                data.loc[i - rownum + 1:i - 1, dict['filed']] = flag  # 地块标志为 非0
                flag += 1
        elif data.loc[i, dict['adjustedToolState']] == 1:  # 当前工作行属于上一工作行所在地块，但与下一工作行不属于一块地
            workPoint2 = data.loc[i, dict['countOfAdjustedSameToolState']]
            rownum += workPoint2
            i += workPoint2
            #  if rownum > cotinuePointThreshold:  # 连续作业 的 轨迹点  少于 10 不能判断 为 地块
            data.loc[i - rownum, dict['filed']] = rownum
            data.loc[i - rownum + 1:i - 1, dict['filed']] = flag  # 地块标志为 非0
            flag += 1
            rownum = 0
        else:  # 非工作行
            if rownum > 0:
                data.loc[i - rownum, dict['filed']] = rownum
                data.loc[i - rownum + 1:i - 1, dict['filed']] = flag  # 地块标志为非0
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
    if data.loc[i, dict['filed']] != 0:  # 地块标志 都不等于 0
        filedNum = data.loc[i, dict['filed']]
        b_lon = list(data.loc[i:i + filedNum - 1, dict['longitude']])
        b_lat = list(data.loc[i:i + filedNum - 1, dict['latitude']])
        x_b, y_b = LoLatitudeChangeToXY_batch(b_lon, b_lat)
        x.extend(x_b)
        y.extend(y_b)
        i += filedNum
    else:
        x.append('a')
        y.append('a')
        i += data.loc[i, dict['countOfAdjustedSameToolState']]

end = time.time()
print('运行时长 {} 秒'.format(end - start))

data.set_index('序列号', inplace=True)

timeStamp = datetime.datetime.now().strftime('%m%d-%H%M%S')
f = file_name.split('.')
# path_name = f[0]+'='+timeStamp+'.'+f[1]

path_name_exl = f[0] + '-' + timeStamp + '.' + f[1]
data.to_excel(path_name_exl)
path_name_csv = f[0] + '-' + timeStamp + '.csv'
data.to_csv(path_name_csv)
