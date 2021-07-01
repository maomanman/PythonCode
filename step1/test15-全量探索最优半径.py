import pandas as pda
import numpy as np
import math
import datetime
import time
import os

import alpha_shape.AlphaShapeForEdge as selfShape
from alpha_shape.ZuoBiaoZhuanHuan import LatLon2GSXY
from alpha_shape.ZuoBiaoZhuanHuan import WGS84ToWebMercator


def test15_2():
    """
    用带轨迹点的回归方差预测最优半径，并进行全量边界检测及面积计算
    :return:
    """
    testpath = r'D:\mmm\实验数据\test15-坐标转换纠正\flag=1'
    filedpath = 'D:\mmm\轨迹数据集\汇总\\'
    imagefilepath = testpath + '/image/'
    edge_path = testpath + '/edgePoint/'

    file_index_data = pda.read_excel(r'D:\mmm\实验数据\test15-坐标转换纠正\flag=1\test15_轨迹索引-v1.0.xlsx')
    result_info = pda.DataFrame(columns=['文件序号', 'edgeNum', '边界点检测耗时', '地块面积', '地块亩数', '最优半径'])
    # errEdge_info = pda.DataFrame(columns=['文件序号', 'edgeNum', '边界点检测耗时', '地块面积', '最优半径', '图片链接'])
    test15_data = pda.read_excel(r'D:\mmm\实验数据\test15-坐标转换纠正\flag=1\test15_result_info.xlsx')
    # result_info.set_index('文件序号',drop=True,inplace=True)
    file_index_data.set_index('新文件序号', drop=True, inplace=True)
    # file_index_data.dropna()

    start_0 = time.time()
    infoIndex = 0

    test15_data = test15_data[test15_data['边界视察'] > 0]

    print("程序开始 {}".format(start_0))
    for i, r in zip(test15_data.index, test15_data.loc[:, '最优半径']):
        fIndex = test15_data.loc[i, '文件序号']  # 获取文件序号
        fileName = file_index_data.loc[fIndex, '文件名称']  # 获取文件名称


        data = selfShape.GetData(filedpath + fileName)  # 读取轨迹文件

        iStr = '{:0>5.0f}'.format(fIndex)  # 文件索引号转换成 5 位长度的 字符串
        print('文件[{}]开始处理'.format(iStr))

        r = round(r + 0.5, 2)
        # print('\t r = %f' % r)

        flag = 1
        while flag:
            print('\t r = %f' % r)
            start = time.time()
            edge_x, edge_y, edge_index = selfShape.alpha_shape_2D(data, r)
            end = time.time()
            # print('\t\t边界检测 完成')

            # 面积计算
            area, times = selfShape.calFiledArea([edge_x, edge_y])  # 根据检测出的边界点计算面积
            # print('\t\t面积计算 完成')

            # 保存边界点
            edge_excel_name = iStr + '_edgePoint_R=' + str(r) + '.xlsx'
            dataTemp=data.set_index('序列号', drop=True)
            edge_data = pda.DataFrame({'pointIndex': edge_index, '经度':dataTemp.loc[edge_index,'经度'],'纬度':dataTemp.loc[edge_index,'纬度'],'x': edge_x, 'y': edge_y})
            edge_data.to_excel(edge_path + edge_excel_name)
            # print('\t\t边界点保存 完成')

            # 绘制边界图
            imagefilepath_r = imagefilepath + iStr + '_' + 'edgeImage_R=' + str(r) + '.jpg'
            selfShape.plotEdgefor12(data, edge_x, edge_y, imagefilepath_r)
            # print('\t\t边界绘制 完成')

            # 登记
            result_info.loc[infoIndex, '文件序号'] = iStr
            result_info.loc[infoIndex, '最优半径'] = r
            # result_info.loc[i, '边界图片链接'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r1, iStr + '_edge')
            # result_info.loc[i, '工作轨迹图片链接'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r2, iStr + '_work')
            # result_info.loc[i, '运动轨迹图片链接'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r3, iStr + '_move')
            # result_info.loc[i, '运动轨迹图片链接(真)'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r4, iStr + '_equalAxe')
            result_info.loc[infoIndex, 'edgepoint'] = edge_excel_name
            result_info.loc[infoIndex, '地块面积'] = area  # 单位 平方米
            result_info.loc[infoIndex, '地块亩数'] = area * 0.0015  # 单位 亩
            result_info.loc[infoIndex, 'edgeNum'] = len(edge_x)
            result_info.loc[infoIndex, '边界点检测耗时'] = round(end - start, 2)

            if infoIndex > 0 and oldArea != 0 :
                oldArea = result_info.loc[infoIndex - 1, '地块面积']
                if (area - oldArea)/oldArea >= 0 and  (area - oldArea)/oldArea < 0.001:
                    flag = 0
                else:
                    r = round(r + 0.5, 2)
            else:
                r = round(r + 0.5, 2)

            if infoIndex % 10 == 0:
                result_info.to_excel(testpath + '/test15_result_info_flag1.xlsx')

            infoIndex = infoIndex + 1


        # print('\t登记 完成')

        del data

        print('\t{}处理完毕'.format(iStr))

    # result_info.set_index('序号', inplace=True)
    result_info.to_excel(testpath + '/test15_result_info_flag1.xlsx')
    end_0 = time.time()
    print("程序结束 {}".format(end_0 - start_0))


test15_2()
