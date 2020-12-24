# coding=utf-8
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd

# path = 'D:/mmm/python/轨迹测试数据/1109-聚类/wholesale.csv'
path = 'D:/mmm/python/轨迹测试数据/1109-聚类/98765_1329.csv'

data = pd.read_csv(path)
# data.drop(["Channel", "Region"], axis=1, inplace=True)

# data = data[["Grocery", "Milk"]]
data = data[["x", "y"]]
data = data.astype("float32", copy=False)#convert to array

#数据预处理，特征标准化，每一维是零均值和单位方差
stscaler = StandardScaler().fit(data)
data = stscaler.transform(data)

#画出x和y的散点图
plt.scatter(data[:, 0], data[:, 1])
plt.xlabel("Groceries")
plt.ylabel("Milk")
plt.title("Wholesale Data - Groceries and Milk")
plt.savefig("D:/mmm/python/轨迹测试数据/1109-聚类/98765_1329.png", format="PNG")

dbsc = DBSCAN(eps=0.02, min_samples=20).fit(data)

labels = dbsc.labels_ #聚类得到每个点的聚类标签 -1表示噪点
print(labels)
core_samples = np.zeros_like(labels, dtype=bool) #构造和labels一致的零矩阵,值是false
core_samples[dbsc.core_sample_indices_] = True
#print(core_samples)


unique_labels = np.unique(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels))) #linespace返回在【0,1】之间均匀分布数字是len个，Sepectral生成len个颜色


#print(zip(unique_labels,colors))
for (label, color) in zip(unique_labels, colors):
    class_member_mask = (labels == label)
    print(class_member_mask&core_samples)
    xy = data[class_member_mask & core_samples]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=color, markersize=10)

    xy2 = data[class_member_mask & ~core_samples]
    plt.plot(xy2[:, 0], xy2[:, 1], 'o-', markerfacecolor=color, markersize=5)
plt.title("DBSCAN on Wholsesale data")
plt.xlabel("Grocery (scaled)")
plt.ylabel("Milk (scaled)")
# plt.show()
plt.savefig("D:/mmm/python/轨迹测试数据/1109-聚类/(0.9,15)dbscan_98765_1329.png", format="PNG")

