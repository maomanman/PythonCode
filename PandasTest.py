# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 00:51:21 2020

@author: Administrator
"""

'''
学习 pandas 的使用

'''

import pandas as pda
import math as ma
import time

# file_name = 'E:/Python/新31-Y3616_2016-10-24=1023-1627-field.csv'

file_name = 'E:/2019首师大/研究课题/农机轨迹分析/深松作业原始数据/新疆/伊犁州/霍城县/新40-60002_2016-04-21.xlsx'
# data = pda.read_csv(file_name)
data = pda.read_excel(file_name)
# print(data['id'])
# print(data['Longitude'])


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

col = len(data.values)

start = time.time()
if '相同机具状态个数' not in data.columns:  # 标签没有则新加入
    dict['countOfSameToolState'] = '相同机具状态个数'  # 将标签名添加到字典中
    data[dict['countOfSameToolState']] = 1
    same_num = 1
    for i in range(1, col):
        if data.loc[i][dict['toolState']] == data.loc[i - 1][dict['toolState']]:
            same_num += 1
        else:
            data.loc[i - same_num:i - 1, dict['countOfSameToolState']] = same_num
            same_num = 1

if '相邻点间隔' not in data.columns:  # 标签没有则新加入
    dict['intervalOfAdjacentPoints'] = '相邻点间隔'
    data[dict['intervalOfAdjacentPoints']] = 0
    for i in range(1, col):
        temp = ma.sin(data.loc[i][dict['latitude']]) * ma.sin(data.loc[i - 1][dict['latitude']]) * ma.cos(
            data.loc[i][dict['longitude']] - data.loc[i - 1][dict['longitude']]) + ma.cos(
            data.loc[i][dict['latitude']]) * ma.cos(data.loc[i - 1][dict['latitude']])
        if temp > 1 or temp < -1:
            # print('i = {},temp = {}'.format(i,temp))
            if data.loc[i][dict['latitude']] == data.loc[i - 1][dict['latitude']] and data.loc[i][dict['longitude']] == \
                    data.loc[i - 1][dict['longitude']]:
                data.loc[i, dict['intervalOfAdjacentPoints']] = 0
        else:
            data.loc[i, dict['intervalOfAdjacentPoints']] = 6371004 * ma.acos(temp) * ma.pi / 180.0

if '调整后机具状态' not in data.columns:  # 标签没有则新加入
    dict['adjustedToolState'] = '调整后机具状态'
    data[dict['adjustedToolState']] = 0
    toolContinum_threshold = 3
    num = 1
    data.loc[:, dict['adjustedToolState']] = data.loc[:, dict['toolState']]
    for i in range(1, col):
        if data.loc[i, dict['countOfSameToolState']] > data.loc[i - 1, dict['countOfSameToolState']]:
            num = data.loc[i - 1, dict['countOfSameToolState']]
            continue
        elif data.loc[i - 1, dict['countOfSameToolState']] <= toolContinum_threshold:
            num = data.loc[i - 1, dict['countOfSameToolState']]
            data.loc[(i - num):i - 1, dict['adjustedToolState']] = data.loc[i - num - 1, dict['adjustedToolState']]

if '调整后相同机具状态个数' not in data.columns:  # 标签没有则新加入
    dict['countOfAdjustedSameToolState'] = '调整后相同机具状态个数'
    data['调整后相同机具状态个数'] = 1
    same_num = 1
    for i in range(1, col):
        if data.loc[i][dict['toolState']] == data.loc[i - 1][dict['toolState']]:
            same_num += 1
        else:
            data.loc[i - same_num:i - 1, dict['countOfSameToolState']] = same_num
            same_num = 1

# 初步计算相同机具状态的平均航向角
if '相同机具状态的平均航向角' not in data.columns:  # 标签没有则新加入
    dict['AverageAngleOfSameToolState'] = '相同机具状态的平均航向角'
    data[dict['AverageAngleOfSameToolState']] = 0
    i = 0
    while i < col:
        sameNum = data.loc[i, dict['countOfAdjustedSameToolState']]
        data.loc[i:(i + sameNum - 1), dict['AverageAngleOfSameToolState']] = ma.fsum(
            data.loc[i:(i + sameNum - 1), dict['angel']])
        i += sameNum

end = time.time()
print('运行时长 {} 秒'.format(end - start))
