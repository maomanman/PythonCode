import pandas as pda



def test21():
    """
    检查轨迹文件中是否存在两点距离较近而时间间隔较远的情况
    :return:
    """
    rootP = r'D:\mmm\轨迹数据集\test21'
    fileP = r'D:\mmm\轨迹数据集\汇总'
    testfile = 'test21-轨迹索引-v1.0.xlsx'
    testfiledata = pda.read_excel(rootP + '/'+ testfile)
    testfiledata.set_index('新文件序号', inplace=True)
    returnfile = pda.DataFrame(columns=['文件名称','最长时间间隔','点序列号起','点序列号止'])

    newid = 0
    for fid  in testfiledata.index:
        filename = testfiledata.loc[fid,'文件名称']
        filedata = pda.read_excel(fileP+'/'+filename)



        count = filedata.shape[0]
        # 先计算相邻两点的时间间隔
        sumTime = pda.to_timedelta(0)
        for ind in range(1, count):
            t1 = filedata.loc[ind - 1, 'GPS时间']
            t2 = filedata.loc[ind, 'GPS时间']
            if type(t2) == str:
                t1 = pda.Timestamp(t1)
                t2 = pda.Timestamp(t2)
                yangT = t2 - t1
            else:
                yangT = t2 - t1
            if yangT.total_seconds() > 4 :
                sumTime = sumTime + yangT
            else:  # 时间间隔大于1分钟的计算两点间距离
                x1, y1 = LatLon2GSXY(data.loc[i - 1, '纬度'], filedata.loc[i - 1, '经度'])
                x2, y2 = LatLon2GSXY(data.loc[i, '纬度'], filedata.loc[i, '经度'])
                d = math.sqrt(pow(y2 - y1, 2) + pow(x2 - x1, 2))
                v = d / yangT.total_seconds()  # m/s

                if v > 1 and v < 2.7778:  # 平均速度 >3.6km/h  <10km/h
                    sumTime = sumTime + yangT