import os
import shutil
import pandas as pda
import math as ma

def moveFile(bastPath='',desPath='',data=''):
    """
    移动文件
    :param bastPath: 源文件路径名
    :param desPath: 目标文件路径名
    :param data: # 待移动文件名
    :return:
    """


    bastPath = r'D:\mmm\实验数据\test15-坐标转换纠正\allPointImage'  # 源文件路径名
    desPath =  r'D:\mmm\实验数据\test15-坐标转换纠正\allPointImage\ALLerr' # 目标文件路径名
    data = pda.read_excel(r'D:\mmm\实验数据\test15-坐标转换纠正\test15_result_info.xlsx')


    # srcList = data[data['边界视察']>0]['edgepoint'] # 待移动文件名列表
    imgaeL=[]
    allL=[]
    axeL=[]
    workL=[]
    for i in data[data['边界视察']>0].index:
        t = data.loc[i,'edgepoint'].replace('Point','Image')

        imgaeL.append(t.replace('xlsx','jpg'))
        allL.append('{:0>5.0f}'.format(data.loc[i,'文件序号'])+'_moveTrajectoryImage.jpg')
        axeL.append('{:0>5.0f}'.format(data.loc[i,'文件序号'])+'_equalAxeTrajectoryImage.jpg')
        workL.append('{:0>5.0f}'.format(data.loc[i,'文件序号'])+ '_workTrajectoryImage.jpg')

    for f in allL:
        srcFile = bastPath + '/'+f
        desFile =desPath + '/' + f
        shutil.move(srcFile,desFile)

    bastPath = r'D:\mmm\实验数据\test15-坐标转换纠正\image'  # 源文件路径名
    desPath = r'D:\mmm\实验数据\test15-坐标转换纠正\image\imageErr'  # 目标文件路径名
    for f in imgaeL:
        srcFile = bastPath + '/'+f
        desFile =desPath + '/' + f
        shutil.move(srcFile,desFile)

    bastPath = r'D:\mmm\实验数据\test15-坐标转换纠正\equalAxeImage'  # 源文件路径名
    desPath = r'D:\mmm\实验数据\test15-坐标转换纠正\equalAxeImage\axeErr'  # 目标文件路径名
    for f in axeL:
        srcFile = bastPath + '/' + f
        desFile = desPath + '/' + f
        shutil.move(srcFile, desFile)

    bastPath = r'D:\mmm\实验数据\test15-坐标转换纠正\justWorkImage'  # 源文件路径名
    desPath = r'D:\mmm\实验数据\test15-坐标转换纠正\justWorkImage\workErr'  # 目标文件路径名
    for f in workL:
        srcFile = bastPath + '/' + f
        desFile = desPath + '/' + f
        shutil.move(srcFile, desFile)

## 登记文件
# def modifyFile():
#     DIR =  'D:/mmm/轨迹数据集/test12/test12_2/edgePoint'
#     def compare(x, y):
#
#         stat_x = os.stat(DIR + "/" + x)
#         stat_y = os.stat(DIR + "/" + y)
#         if stat_x.st_ctime < stat_y.st_ctime:
#             return -1
#         elif stat_x.st_ctime > stat_y.st_ctime:
#             return 1
#         else:
#             return 0
#
#     path =  'D:/mmm/轨迹数据集/test12/test12_2/edgePoint'
#     fp=r'D:\mmm\轨迹数据集\test12\test12_2\errEdge_info -01.xlsx'
#
#     data = pda.read_excel(fp)
#
#     edgList = os.listdir(path)
#     edgList.sort(key=lambda fn: os.path.getmtime(path+'/'+fn))
#     for i in data.index:
#         data.loc[i,'edgepoint'] = edgList[i]
#
#     data.to_excel(fp)

def listDir():

    edgePointP = basePath + '/edgePoint-01'
    allPointImageP = basePath + '/allPointImage-01'
    equalImageP = basePath + '/equalImage-01'
    imageP =  basePath + '/image-01'
    justWorkImageP = basePath + '/justWorkImage-01'

    list1 = os.listdir(edgePointP)
    list2 = os.listdir(imageP)
    list3 = os.listdir(allPointImageP)
    list4 = os.listdir(equalImageP)
    list5 = os.listdir(justWorkImageP)

    data = pda.read_excel(basePath+'/test12_图片列表.xlsx')
    data.set_index('新文件序号',drop=True,inplace=True)
    for i in range(0,len(list1)):
        fileIndex = int(list1[i].split('_')[0])
        if list1[i].split('_')[0] != list2[i].split('_')[0] or  list1[i].split('_')[0] != list3[i].split('_')[0] or list1[i].split('_')[0] != list4[i].split('_')[0] or list1[i].split('_')[0] != list5[i].split('_')[0]:
            print(list1[i].split('_')[0])
            print(list2[i].split('_')[0])
            print(list3[i].split('_')[0])
            print(list4[i].split('_')[0])
            print(list5[i].split('_')[0])
            break
        data.loc[fileIndex,'edgePoint'] = list1[i]
        data.loc[fileIndex, 'image'] = list2[i]
        data.loc[fileIndex, 'allPointImage'] = list3[i]
        data.loc[fileIndex, 'equalImage'] = list4[i]
        data.loc[fileIndex, 'justWorkImage'] = list5[i]

        if i % 10 ==0 :
            data.to_excel(basePath+'/test12_图片列表.xlsx')

    data.to_excel(basePath + '/test12_图片列表.xlsx')

def calFiledArea(edge):
    """
    根据边界点 利用多边形计算公式 计算地块面积
    :param edge: 地块边界点(默认是dataframe格式)
    :return: 地块面积，以及面积计算时长
    """
    if type(edge) != pda.pandas.core.frame.DataFrame:
        t = pda.DataFrame(columns=['x', 'y'])
        t.x = edge[0]
        t.y = edge[1]
        edge = t

    count = edge.shape[0] - 1  # 获取边界点个数
    i = 0
    temp = 0
    area = 0
    # 多边形面积计算

    while i < count:
        temp += edge.x[i] * edge.y[i + 1] - edge.x[i + 1] * edge.y[i]
        i += 1
    area = 0.5 * ma.fabs(temp)  # 平方米  （多边形顶点按逆时针排列则是正值，顺时针排列则是负值）


    # print(times)

    return area

def batchCalAreas():
    edgepointP = basePath + '/edgePoint-01'
    data = pda.read_excel(basePath+'/test12_图片列表.xlsx')
    data.set_index('新文件序号',inplace=True,drop=True)
    for i,edp in zip(data.index,data.loc[:,'edgePoint']):
        if type(edp) != str:
            continue
        edgeF = edgepointP +'/'+edp
        edge = pda.read_excel(edgeF)
        area = calFiledArea(edge) # 平方
        data.loc[i,'作业面积平方'] = area
        data.loc[i, '作业面积亩'] = area * 0.0015
        if i % 10 == 0:
            data.to_excel(basePath + '/test12_图片列表.xlsx')

    data.to_excel(basePath + '/test12_图片列表.xlsx')

basePath = r'D:\mmm\轨迹数据集\test12'

# listDir()
# batchCalAreas()
#
# mkt=[[11374.541,12475.244,11935.923],[11549.98,12667.92,12121.23]]
# gst=[[11548.98,12667.92,12121.23],[45135.464,46006.668,43675.679]]
# mareas =calFiledArea(mkt)
# gsareas=calFiledArea(gst)
#
# print('墨卡托：{}'.format(mareas))
# print('高斯：{}'.format(gsareas))

moveFile()