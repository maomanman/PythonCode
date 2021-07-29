import pandas as pda
import numpy as np
import math
import datetime
import time

import alpha_shape.AlphaShapeForEdge as selfShape
from alpha_shape.ZuoBiaoZhuanHuan import LatLon2GSXY
from alpha_shape.ZuoBiaoZhuanHuan import WGS84ToWebMercator


def test15():
    """
    最终获取边界点及边界图
    :return:
    """
    testpath = r'D:\mmm\实验数据\test15-坐标转换纠正\flag=2' # 测试路径
    filedpath = 'D:\mmm\轨迹数据集\汇总\\' # 轨迹点文件存放路径
    imagefilepath = testpath + '/image/' # 边界图存放路径
    edge_path = testpath + '/edgePoint/' # 边界点存放路径

    file_index_data = pda.read_excel(r'D:\mmm\实验数据\test15-坐标转换纠正\flag=2\test15_轨迹索引-v1.0.xlsx')
    test15_radius_data  = pda.read_excel(r'D:\mmm\实验数据\test15-坐标转换纠正\flag=2\test15_result_info.xlsx')
    result_info = pda.DataFrame(columns=['文件序号', 'edgeNum', '边界点检测耗时', '地块面积','地块亩数', '最优半径'])
    file_index_data.set_index('新文件序号',drop=True,inplace=True)

    start_0 = time.time()

    test15_radius_data= test15_radius_data[test15_radius_data['边界视察']==2]


    print("程序开始 {}".format(start_0))
    for i ,r in zip(test15_radius_data.index,test15_radius_data.loc[:,'最优半径']):

        fIndex=test15_radius_data.loc[i,'文件序号']
        f=file_index_data.loc[fIndex,'文件名称']

        iStr = '{:0>5.0f}'.format(fIndex) # 将文件序号转换成字符串，方便后面用此序号给图片及边界点文件命名

        print(fIndex)
        print(f)

        data = selfShape.GetData(filedpath + f)

        # 边界检测
        start = time.time()
        edge_x, edge_y, edge_index = selfShape.alpha_shape_2D(data, r)
        end = time.time()
        # print('\t边界检测 完成')
        #
        # 面积计算
        area, times =selfShape.calFiledArea([edge_x, edge_y])  # 根据检测出的边界点计算面积
        # print('\t面积计算 完成')
        #
        # # 保存边界点
        data.set_index('序列号',drop=True,inplace=True)
        edge_excel_name = iStr + '_edgePoint_R=' + str(round(r, 2)) + '.xlsx'
        edge_data = pda.DataFrame({'pointIndex': edge_index,'经度':data.loc[edge_index,'经度'],'纬度':data.loc[edge_index,'纬度'],'x': edge_x, 'y': edge_y})
        edge_data.reset_index(drop=True,inplace=True)
        edge_data.to_excel(edge_path + edge_excel_name)
        # print('\t边界点保存 完成')

        # 绘制边界图
        imagefilepath_r1 = imagefilepath + iStr + '_' + 'edgeImage_R=' + str(round(r, 2)) + '.jpg'
        imagefilepath_r2 = testpath + '/justWorkImage/' + iStr + '_' + 'workTrajectoryImage' + '.jpg'
        imagefilepath_r3 = testpath + '/allPointImage/' + iStr + '_' + 'moveTrajectoryImage' + '.jpg'
        imagefilepath_r4 = testpath + '/equalAxeImage/' + iStr + '_' + 'equalAxeTrajectoryImage' + '.jpg'

        # # # plotEdge(data.x, data.y, edge_x, edge_y) # 只绘制，不保存
        # plotEdgefor12(data, edge.x, edge.y)
        # plotEdgefor12(data, edge_x, edge_y)
            # mine = float(input("0-跳过 r = "))

        # #
        selfShape.plotEdgefor12(data, edge_x, edge_y, imagefilepath_r1)
        selfShape.plotEdgefor12(data, edge_x, edge_y, imagefilepath_r2)
        selfShape.plotEdgefor12(data, edge_x, edge_y, imagefilepath_r3)
        selfShape.plotEdgefor12(data, edge_x, edge_y, imagefilepath_r4)
        # # print('\t边界绘制 完成')

        result_info.loc[i, '文件序号']=iStr
        result_info.loc[i, '最优半径'] = r
        result_info.loc[i, '边界图片链接'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r1, iStr + '_edge')
        result_info.loc[i, '工作轨迹图片链接'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r2, iStr + '_work')
        result_info.loc[i, '运动轨迹图片链接'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r3, iStr + '_move')
        result_info.loc[i, '运动轨迹图片链接(真)'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r4, iStr + '_equalAxe')
        result_info.loc[i, 'edgepoint'] = edge_excel_name
        result_info.loc[i, '地块面积'] = area  # 单位 平方米
        result_info.loc[i, '地块亩数'] = area * 0.0015  # 单位 亩
        result_info.loc[i, 'edgeNum'] = len(edge_x)
        result_info.loc[i, '边界点检测耗时'] = round(end-start,2)
        #

        print('\t登记 完成')
        del data
        # del edge

        print('\t{}处理完毕'.format(iStr))


        if i % 10 == 0:  # 每登记10个保存一次
            result_info.to_excel(testpath + '/test15_result_info_flag2.xlsx')



    result_info.to_excel(testpath + '/test15_result_info_flag2.xlsx')
    end_0 = time.time()
    print("程序结束 {}".format(end_0 - start_0))




test15()