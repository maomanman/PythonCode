import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# # 生成数据
# v1 = np.random.normal(0, 1, 100)
# v2 = np.random.randint(0, 23, 100)
# v3 = v1 * v2
#
# # 3*100 的数据框
# df = pd.DataFrame([v1, v2, v3]).T
data = pd.read_excel(r'D:\mmm\实验数据\test26-计算地块周长\test26-相关矩阵图数据-test.xlsx')
data2 = pd.read_excel(r'D:\mmm\实验数据\test26-计算地块周长\test26-相关矩阵图数据-test2.xlsx')



# df = data.apply(np.log10)
# df = data
# df.drop(columns=['总工作时长秒','工作总时长小时','有效工作时长秒'],inplace=True)
# df = df.apply(np.log10)
#
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus']=False # 显示负号
# # 绘制散点图矩阵
#
# pd.plotting.scatter_matrix(df)
data3= data2[data2['工作行程']<20000]

x = np.linspace(0,100,data3.shape[0])

plt.scatter(x[:],data3.工作行程,c='b')
plt.scatter(x[:],data3.工作行程2,c='r')
plt.legend({'行程量1','行程量2'})
plt.show()