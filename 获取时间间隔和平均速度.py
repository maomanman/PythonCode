import pandas as pda



def getTimeAndSpeed(filepath):
    """
    根据某个文件路径获取其采样间隔和平均速度
    :param path: 文件路径
    :return: 返回速度是 m/s  时间是s
    """
    filedata = pda.read_excel(filepath)  # 读取轨迹文件
    filedata.rename(columns={'速度(km/h)': 'speed'}, inplace=True)
    workPoint = filedata[filedata.工作状态 == True]
    speedMean = workPoint.speed.sum() / workPoint.shape[0]  # 根据工作状态中的点速度求平均速度
    # fIndex = edgeInfoData[edgeInfoData.文件名==f].index
    # edgeInfoData.loc[t, vStr] = speedMean  # 登记平均速度

    # 计算时间间隔
    filepointCount = filedata.shape[0]
    for i in range(1, filepointCount):

        if type(filedata.loc[i, 'GPS时间']) == str:
            startTime = pda.Timestamp(filedata.loc[i - 1, 'GPS时间'])
            endTime = pda.Timestamp(filedata.loc[i, 'GPS时间'])
        else:
            startTime = filedata.loc[i - 1, 'GPS时间']
            endTime = filedata.loc[i, 'GPS时间']
        filedata.loc[i, '时间间隔'] = (endTime - startTime).seconds


    return speedMean*0.2777778 ,filedata.时间间隔.mode()[0]


def batch_getTimeAndSpeed():
    """
    批量获取采样间隔和平均速度
    :return:
    """
    path = r'D:\mmm\轨迹数据集\image-最多轨迹点文件\widthInfo-汇总比较-pcharm.xlsx'
    edgeInfoData = pda.read_excel(path)
    datapath = r'D:\mmm\轨迹数据集\汇总'

    for num in range(1,4):
        filenameStr = '文件名称'+str(num)
        t=0
        vStr = '平均速度' +str(num)
        timeStr =  '采样间隔时间' + str(num)
        for f in edgeInfoData.loc[:, filenameStr]:  # 获取文件名称
            filepath = datapath + '/' + f

            speedMean,yangTime=getTimeAndSpeed(filepath)
            edgeInfoData.loc[t, vStr] = speedMean  # 登记平均速度
            edgeInfoData.loc[t, timeStr] = yangTime  # 登记采样时间

            # filedata = pda.read_excel(filepath)  # 读取轨迹文件
            # filedata.rename(columns={'速度(km/h)': 'speed'}, inplace=True)
            # workPoint = filedata[filedata.工作状态 == True]
            # speedMean = workPoint.speed.sum() / workPoint.shape[0]  # 根据工作状态中的点速度求平均速度
            # # fIndex = edgeInfoData[edgeInfoData.文件名==f].index
            # edgeInfoData.loc[t, vStr] = speedMean  # 登记平均速度
            #
            # # 计算时间间隔
            # filepointCount = filedata.shape[0]
            # for i in range(1, filepointCount):
            #
            #     if type(filedata.loc[i, 'GPS时间']) == str:
            #         startTime = pda.Timestamp(filedata.loc[i - 1, 'GPS时间'])
            #         endTime = pda.Timestamp(filedata.loc[i, 'GPS时间'])
            #     else:
            #         startTime = filedata.loc[i - 1, 'GPS时间']
            #         endTime = filedata.loc[i, 'GPS时间']
            #     filedata.loc[i, '时间间隔'] = (endTime - startTime).seconds
            #
            # # edgeInfoData.loc[t,'采样间隔时间'] = filedata.时间间隔.mode()
            # edgeInfoData.loc[t, timeStr] = filedata.时间间隔.mode()[0]
            print(t)

            # print(filedata.时间间隔.mode())
            # print(fIndex)
            # print(edgeInfoData.loc[t, '采样间隔时间'])
            t = t + 1
            # if '449' in f:
            #     print(f)
            # print(f)
            # del filedata

    edgeInfoData.set_index('序号', inplace=True)
    edgeInfoData.to_excel(path)


filepath = r'D:\mmm\轨迹数据集\汇总\00378 耕-中-套==鲁01_531538_2017-9-29==0928-2344-filed.xlsx'
s,t=getTimeAndSpeed(filepath)
print(s,t)