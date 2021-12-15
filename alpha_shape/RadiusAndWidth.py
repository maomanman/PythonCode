import pandas as pda
import numpy as np



def findRadius():
    """
    搜寻合适的圆半径
    :return:
    """
    path = 'D:/mmm/python/轨迹测试数据/1106-半径优化'
    f_r = '湘12-E1136_2016-10-13==1013-0746-field.csv'
    f_t = '皖17-80100_2016-10-07==1006-2357-field.csv'
    f_s = '新42-98765_2016-11-10==1109-2117-field.csv'
    imagepath_r = path + '/image/' + f_r.replace('.csv', '-image.png')
    imagepath_t = path + '/image/' + f_t.replace('.csv', '-image.png')
    imagepath_s = path + '/image/' + f_s.replace('.csv', '-image.png')
    imagepath = [imagepath_r, imagepath_t, imagepath_s]
    data_r = GetData(path + '/' + f_r)  # 绕行
    data_t = GetData(path + '/' + f_t)  # 套行
    data_s = GetData(path + '/' + f_s)  # 梭行
    datas = [data_r, data_t, data_s]
    # radius = np.linspace(1, 10, 10)  # 设置半径的选项值
    # radius = np.linspace(3, 10, 15)  # 设置半径的选项值
    # radius = np.linspace(5, 8, 16)  # 设置半径的选项值
    radius = np.linspace(5, 5.6, 13)  # 设置半径的选项值
    radiusInfo = pda.DataFrame(columns=['radius', 'edgeNum', 'pointNum', '耗时', '边界占比率'])
    i = 0
    for r in radius:
        for data, im in zip(datas, imagepath):
            start = time.time()
            edge_x, edge_y, edge_index = alpha_shape_2D(data, r)
            end = time.time()
            radiusInfo.loc[i] = [r, len(edge_x), data.shape[0], end - start, len(edge_x) / data.shape[0]]
            i += 1
            im = im.replace('.', '-' + str(r) + '.')
            plotEdge(data.x, data.y, edge_x, edge_y, im)

    radiusInfo.to_excel(path + '/radiusInfo=50-56.xlsx')
    del radiusInfo