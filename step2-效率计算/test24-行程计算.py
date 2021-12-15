import pandas as pda
import  time
import alpha_shape.AlphaShapeForEdge as selfShape




def test24_maxTrip():
    """
    检测每个轨迹文件中，相邻两点的最大距离
    :return:
    """


def test24_totalTripOfAfile(fileName):
    """
    计算一个文件的总行程
    :return:
    """
    testPath = r'D:\mmm\实验数据\test24-行程计算'

    data = selfShape.GetData('D:/mmm/轨迹数据集/汇总/' + fileName)
    # data.to_excel(testPath + '/' + fileName)
    x0 = data.loc[0,'x']
    y0 = data.loc[0,'y']
    tripSum = 0
    for x,y in zip(data.loc[:,'x'],data.loc[:,'y']):
        tripSum =tripSum + selfShape.distance((x0,y0),(x,y))
        x0 = x
        y0 = y

    # print(tripSum)
    return tripSum





def test24_workTripOfAfile(fileName,yangT):
    """
    计算一个文件的工作行程
    :return:
    """
    # testPath = r'D:\mmm\实验数据\test24-行程计算'

    data = selfShape.GetData('D:/mmm/轨迹数据集/汇总/' + fileName)
    data = data[data['工作状态'] == True]   # 筛选 工作中的的点
    data.reset_index(inplace=True)
    i = 1
    count = data.shape[0]

    tripSum = 0

    while i <  count:
        index0 = data.loc[i-1,'序列号']
        index1 = data.loc[i, '序列号']

        if index1 - index0 ==1:
            x0 = data.loc[i-1, 'x']
            y0 = data.loc[i-1, 'y']
            x = data.loc[i , 'x']
            y = data.loc[i, 'y']

            tripSum = tripSum+ selfShape.distance((x0,y0),(x,y))
        else:
            tripSum = tripSum + data.loc[i-1,'速度(km/h)'] *  0.27778 * yangT

        i= i + 1

    # print(tripSum)
    return tripSum

def TripOfAfile(fileName,yangT):
    """
    计算行程量：根据每个点的作业状态、作业速度、采样时间
    :param fileName:
    :param yangT:
    :return:
    """
    workTrip = 0
    totalTrip = 0
    data = selfShape.GetData('D:/mmm/轨迹数据集/汇总/' + fileName)

    for v,st, in zip(data.loc[:,'速度(km/h)'],data.loc[:,'工作状态']):
        v = v * 1000/3600
        if st:
            workTrip += v * yangT
        totalTrip += v * yangT

    return workTrip,totalTrip

def batch_Trip():
    """

    :return:
    """
    indexF = pda.read_excel(r'D:\mmm\实验数据\test24-行程计算\test24-轨迹索引-v3.0.xlsx')
    test24_result = pda.DataFrame(columns={'文件序号','工作行程','总行程量'})
    i= 0
    for fileName,yangT in zip(indexF.loc[:,'文件名称'],indexF.loc[:,'采样时间']):
        print(fileName,yangT)
        # workTrip,totalTrip = TripOfAfile(fileName, yangT)

        workTrip = test24_workTripOfAfile(fileName, yangT)
        totalTrip = test24_totalTripOfAfile(fileName)

        test24_result.loc[i]=[fileName[0:5],workTrip,totalTrip]
        i += 1

    test24_result.to_excel(r'D:\mmm\实验数据\test24-行程计算\test24_result_trip_2.xlsx')





# fileName = '00012 耕-大-斜==黑02-S45271_2019-10-4==1003-2137-filed.xlsx'
# yangT = 4
#
# # 测试一个文件的 总行程长度
# test24_totalTripOfAfile(fileName)
# # 测试一个文件的 工作行程长度
# test24_workTripOfAfile(fileName,yangT)
#
# print(TripOfAfile(fileName,yangT))

batch_Trip()