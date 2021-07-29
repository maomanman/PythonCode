import pandas as pda
import numpy as np
import  time
import os
import alpha_shape.AlphaShapeForEdge as selfShape


# 整理所有地块的标志 是否可用
def test23():

    rootPath = r'D:\mmm\实验数据\test23-中期信息整理'
    test23_data_index = pda.read_excel(rootPath  + '/test23_data_index_updata.xlsx')
    test15_result_data = pda.read_excel(rootPath  + '/test23-test15_result_info.xlsx')
    test23_data_index.set_index('新文件序号',drop=True,inplace=True)
    test15_result_data.set_index('文件序号',drop=True,inplace=True)

    test23_data_index_temp = test23_data_index[test23_data_index['地块标志'] ==0]

    for fIndex in test23_data_index_temp.index :
        # fIndex = test15_result_data.loc[i,'文件序号']
        # fFlag = test15_result_data.loc[i,'半径是否可行']
        # if fFlag == 1 :
        #     test23_data_index.loc[fIndex,'最优半径']=test15_result_data.loc[i,'最优半径']
        # elif fFlag == 2 :
        #     test23_data_index.loc[fIndex, '地块标志'] = 3
        if test23_data_index_temp.loc[fIndex,'最优半径'] == 0:
            test23_data_index.loc[fIndex,'最优半径'] = test15_result_data.loc[fIndex,'最优半径']

    test23_data_index.to_excel(rootPath + '/test23_data_index_updata2.xlsx')


def test23_flag():
    """
    对边界有缺陷，且未知最优半径的地块进行全量探索最优半径
    :return:
    """
    testpath = r'D:\mmm\实验数据\test23-中期信息整理'
    filedpath = 'D:\mmm\轨迹数据集\汇总\\'
    imagefilepath = testpath + '/image/'
    edge_path = testpath + '/edgePoint/'

    file_index_data = pda.read_excel(testpath +'/test23_data_index_flag = 1.xlsx')
    result_info = pda.DataFrame(columns=['文件序号', 'edgeNum', '边界点检测耗时', '地块面积', '地块亩数', '最优半径'])
    # errEdge_info = pda.DataFrame(columns=['文件序号', 'edgeNum', '边界点检测耗时', '地块面积', '最优半径', '图片链接'])
    test23_data = pda.read_excel(r'D:\mmm\实验数据\test15-坐标转换纠正\flag=1\test15_result_info_flag1.xlsx')
    # result_info.set_index('文件序号',drop=True,inplace=True)
    file_index_data.set_index('新文件序号', drop=True, inplace=True)
    # file_index_data.dropna()

    start_0 = time.time()
    infoIndex = 0

    test23_data = file_index_data[file_index_data['地块标志'] > 0]
    test23_data = test23_data[test23_data['最优半径']==0]

    print("程序开始 {}".format(start_0))
    r= 0.5
    for fIndex in test23_data.index:
        # fIndex = test23_data.loc[i, '文件序号']  # 获取文件序号
        fileName = test23_data.loc[fIndex, '文件名称']  # 获取文件名称


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


            if infoIndex > 0 and result_info.loc[infoIndex - 1, '地块面积'] != 0 :
                oldArea = result_info.loc[infoIndex - 1, '地块面积']
                if (area - oldArea)/oldArea >= 0 and  (area - oldArea)/oldArea < 0.0001:
                    flag = 0
                else:
                    r = round(r + 0.5, 2)
            else:
                r = round(r + 0.5, 2)

            if infoIndex % 10 == 0:
                result_info.to_excel(testpath + '/test23_result_info_flag_r==0.xlsx')

            infoIndex = infoIndex + 1


        # print('\t登记 完成')

        del data

        print('\t{}处理完毕'.format(iStr))

    # result_info.set_index('序号', inplace=True)
    result_info.to_excel(testpath + '/test23_result_info_flag_r==0.xlsx')
    end_0 = time.time()
    print("程序结束 {}".format(end_0 - start_0))

def test23_r():
    """
    对边界有缺陷，但已知最优半径的地块进行边界绘制
    :return:
    """
    testpath = r'D:\mmm\实验数据\test23-中期信息整理'
    filedpath = 'D:\mmm\轨迹数据集\汇总\\'
    imagefilepath = testpath + '/image/'
    edge_path = testpath + '/edgePoint/'

    file_index_data = pda.read_excel(testpath +'/test23_data_index_updata2.xlsx')
    result_info = pda.DataFrame(columns=['文件序号', 'edgeNum', '边界点检测耗时', '地块面积', '地块亩数', '最优半径'])
    # errEdge_info = pda.DataFrame(columns=['文件序号', 'edgeNum', '边界点检测耗时', '地块面积', '最优半径', '图片链接'])
    # test23_data = pda.read_excel(r'D:\mmm\实验数据\test15-坐标转换纠正\flag=1\test15_result_info_flag1.xlsx')
    # result_info.set_index('文件序号',drop=True,inplace=True)
    file_index_data.set_index('新文件序号', drop=True, inplace=True)
    # file_index_data.dropna()

    start_0 = time.time()
    infoIndex = 0

    test23_data = file_index_data[file_index_data['地块标志'] > 0]
    # test23_data = test23_data[test23_data['最优半径']>0] # 已知半径

    print("程序开始 {}".format(start_0))
    # r= 0.5
    for fIndex,r in zip(test23_data.index,test23_data['最优半径']):
        # fIndex = test23_data.loc[i, '文件序号']  # 获取文件序号
        fileName = test23_data.loc[fIndex, '文件名称']  # 获取文件名称


        data = selfShape.GetData(filedpath + fileName)  # 读取轨迹文件

        iStr = '{:0>5.0f}'.format(fIndex)  # 文件索引号转换成 5 位长度的 字符串
        print('文件[{}]开始处理'.format(iStr))

        # r = round(r + 0.5, 2)
        # print('\t r = %f' % r)


        # print('\t r = %f' % r)
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
        imagefilepath_r1 = imagefilepath + iStr + '_' + 'edgeImage_R=' + str(round(r, 2)) + '.jpg'
        imagefilepath_r2 = testpath + '/justWorkImage/' + iStr + '_' + 'workTrajectoryImage' + '.jpg'
        imagefilepath_r3 = testpath + '/allPointImage/' + iStr + '_' + 'moveTrajectoryImage' + '.jpg'
        imagefilepath_r4 = testpath + '/equalAxeImage/' + iStr + '_' + 'equalAxeTrajectoryImage' + '.jpg'

        # 绘制边界图
        imagefilepath_r = imagefilepath + iStr + '_' + 'edgeImage_R=' + str(r) + '.jpg'
        selfShape.plotEdgefor12(data, edge_x, edge_y, imagefilepath_r)


        # print('\t\t边界绘制 完成')

        # #
        selfShape.plotEdgefor12(data, edge_x, edge_y, imagefilepath_r1)
        selfShape.plotEdgefor12(data, edge_x, edge_y, imagefilepath_r2)
        selfShape.plotEdgefor12(data, edge_x, edge_y, imagefilepath_r3)
        selfShape.plotEdgefor12(data, edge_x, edge_y, imagefilepath_r4)

        # 登记
        result_info.loc[infoIndex, '文件序号'] = iStr
        result_info.loc[infoIndex, '最优半径'] = r
        result_info.loc[infoIndex, '边界图片链接'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r1, iStr + '_edge')
        result_info.loc[infoIndex, '工作轨迹图片链接'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r2, iStr + '_work')
        result_info.loc[infoIndex, '运动轨迹图片链接'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r3, iStr + '_move')
        result_info.loc[infoIndex, '运动轨迹图片链接(真)'] = '=HYPERLINK("{}","{}")'.format(imagefilepath_r4, iStr + '_equalAxe')
        result_info.loc[infoIndex, 'edgepoint'] = edge_excel_name
        result_info.loc[infoIndex, '地块面积'] = area  # 单位 平方米
        result_info.loc[infoIndex, '地块亩数'] = area * 0.0015  # 单位 亩
        result_info.loc[infoIndex, 'edgeNum'] = len(edge_x)
        result_info.loc[infoIndex, '边界点检测耗时'] = round(end - start, 2)
        file_index_data.loc[fIndex,'地块标志'] = 0


        # if infoIndex > 0 and result_info.loc[infoIndex - 1, '地块面积'] != 0 :
        #     oldArea = result_info.loc[infoIndex - 1, '地块面积']
        #     if (area - oldArea)/oldArea >= 0 and  (area - oldArea)/oldArea < 0.0001:
        #         flag = 0
        #     else:
        #         r = round(r + 0.5, 2)
        # else:
        #     r = round(r + 0.5, 2)

        if infoIndex % 10 == 0:
            result_info.to_excel(testpath + '/test23_result_info_all.xlsx')

        infoIndex = infoIndex + 1


        # print('\t登记 完成')

        del data

        print('\t{}处理完毕'.format(iStr))

    # result_info.set_index('序号', inplace=True)
    result_info.to_excel(testpath + '/test23_result_info_all.xlsx')
    file_index_data.to_excel(testpath +'/test23_data_index_updata3.xlsx')
    end_0 = time.time()
    print("程序结束 {}".format(end_0 - start_0))

def test23_batchCalAreasByEdgePoint():
    """
    批量计算面积，根据边界点
    :return:
    """
    testpath =r'D:\mmm\实验数据\test23-中期信息整理'
    edgePointFile = os.listdir(testpath+'/edgePoint')
    fileIndexFile= pda.read_excel(testpath+'/test23-中期汇总-轨迹索引-v1.0.xlsx')
    fileIndexFile.set_index('新文件序号',drop=True,inplace=True)

    test23_result =pda.DataFrame(columns={'文件名称','作业面积','作业面积亩'})

    for f in edgePointFile:
        fileIndex = np.int64(f[0:5])
        edgeData = pda.read_excel(testpath+'/edgePoint/'+ f)
        area,times = selfShape.calFiledArea(edgeData)
        areaM =  area * 0.0015


        test23_result.loc[fileIndex]=[fileIndexFile.loc[fileIndex,'文件名称'],area,areaM]

        if fileIndex % 10 == 0:
            test23_result.to_excel(testpath + '/test23_作业面积汇总.xlsx')


    test23_result.to_excel(testpath + '/test23_作业面积汇总.xlsx')



# test23()
# test23_flag()
# test23_r()

# selfShape.justShowEdge('00986 收-小-绕==皖18-04682_2019-11-11==1111-0029-filed.xlsx',8.66)
test23_batchCalAreasByEdgePoint()