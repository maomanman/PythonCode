import scipy.stats as stats  # 用于正态性检验
from sklearn import preprocessing # 用于处理数据的 -- 归一化

import pandas as pd

rootPath = r'D:\mmm\实验数据\相关性分析'

# 归一化
def test41_prepareData():

    data = pd.read_excel(rootPath + '/step4-作业效率汇总.xlsx')
    data['作业效率归一化'] = preprocessing.minmax_scale(data.loc[:,'作业效率（m2/s）'])
    data.to_excel(rootPath + '/step4-作业效率汇总-归一化.xlsx')

    return  data

# 第一步 ： 正态性检验
def test41_step1(data):

    # r_data = data[data.作业模式 == '绕行法']
    # t_data = data[data.作业模式 == '套行法']
    # s_data = data[data.作业模式 == '梭行法']
    # x_data = data[data.作业模式 == '斜行法']
    # rs = stats.shapiro(r_data.loc[:,'作业效率（m2/s）'])
    # ts = stats.shapiro(t_data.loc[:, '作业效率（m2/s）'])
    # ss = stats.shapiro(s_data.loc[:, '作业效率（m2/s）'])
    # xs = stats.shapiro(x_data.loc[:, '作业效率（m2/s）'])

    # print(rs)
    # print(ts)
    # print(ss)
    # print(xs)

    print(data.shape)
    print(stats.shapiro(data.loc[:, '作业效率归一化']))



#特征工程
def Standardization():
    """
    x = (x-均值)/标准差
    方差= sum(pow((x-均值),2))
    :return:
    """
    data = pd.read_excel(rootPath + '/test41-data.xlsx')

    x = preprocessing.scale(data) # 每一个列按正态分布进行标准化，归一化后有正有负
    # print(x)
    # 最大值最小值归一化
    x2 = preprocessing.minmax_scale(data)
    print(x2)

# test41_step1(test41_prepareData())
Standardization()


