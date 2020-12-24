"""
optics算法主程序
"""
# -*- coding: utf-8 -*-

import numpy as np
from itertools import count
from matplotlib import pyplot as plt
from scipy.spatial.distance import euclidean
from collections import defaultdict
from sklearn.cluster import DBSCAN
from sklearn import datasets
from matplotlib.pyplot import cm

from kd_tree import KDTree
from heap import Heap
from verbose import Verbose

import pandas as pad
from sklearn.preprocessing import StandardScaler

class OPTICS(Verbose):
    def __init__(self,
                 max_eps=0.5,
                 min_samples=10,
                 metric=euclidean,
                 verbose=True):
        self.max_eps = max_eps
        self.min_samples = min_samples
        self.metric = metric
        super(OPTICS, self).__init__(verbose)

    def _get_neighbors(self, point_id):
        """计算数据点的eps-邻域，同时也得到core-distance
        :param point_id:
        :returns:
        :rtype:

        """
        point = self.kd_tree[point_id]
        neighbors = self.kd_tree.query_ball_point(point, self.max_eps)
        ## 把节点本身排除在外
        neighbors.pop(0)

        if len(neighbors) < self.min_samples:
            core_distance = np.inf
        else:
            core_distance = neighbors[self.min_samples - 1][0]

        return [x[1] for x in neighbors], core_distance

    def _update(self, order_seeds, neighbors, point_id):
        """

        :returns:
        :rtype:
        """
        ## 能进到这个函数的core_distance都是满足core_distance<np.inf的
        core_distance = self.results[point_id][1]
        for neighbor in neighbors:
            ## 如果该邻域点没有处理过，更新reachability_distance
            ## 注意:如果某个点已经处理过（计算core_distance并作为point_id进入该函数），那么
            ## 该点的reachability_distance就不会再被更新了，即采用“先到先得”的模式
            if not self.results[neighbor][0]:
                self.printer("节点{}尚未处理，计算可达距离".format(neighbor))
                new_reachability_distance = max(core_distance,
                                                self.metric(
                                                    self.kd_tree[point_id],
                                                    self.kd_tree[neighbor]))

                ## 如果新的reachability_distance小于老的，那么进行更新，否则不更新
                if new_reachability_distance < self.results[neighbor][2]:
                    self.printer("节点{}的可达距离从{}缩短至{}".format(
                        neighbor, self.results[neighbor][2],
                        new_reachability_distance))
                    self.results[neighbor][2] = new_reachability_distance
                    ## 对新数据执行插入，对老数据执行decrease_key
                    order_seeds.push([new_reachability_distance, neighbor])

    def _expand_cluste_order(self, point_id):
        """ FIXME briefly describe function


        :param point_id:
        :returns:
        :rtype:

        """

        neighbors, core_distance = self._get_neighbors(point_id)
        self.printer("节点{}的邻域点数量为{},核心距离为{}".format(point_id, len(neighbors),
                                                    core_distance))
        self.results[point_id][0] = True  # 标记为已处理
        self.results[point_id][1] = core_distance
        if(not self.results_order.count(point_id)):
            self.results_order.append(point_id)  # 记录数据点被处理的顺序
        if core_distance < np.inf:
            self.printer("节点{}为核心点，递归处理其邻域".format(point_id))
            ## order_seeds是以reachability_distance为key，point_id为handle的优先队列（堆）
            order_seeds = Heap(verbose=False)
            data = [[self.results[x][2], x] for x in neighbors]
            order_seeds.heapify(data)
            self._update(order_seeds, neighbors, point_id)
            while not order_seeds.is_empty:
                _, current_point_id = order_seeds.pop()
                neighbors, core_distance = self._get_neighbors(
                    current_point_id)
                self.printer("节点{}的邻域点数量为{},核心距离为{}".format(
                    current_point_id, len(neighbors), core_distance))
                self.results[current_point_id][0] = True  # 标记为已处理
                self.results[current_point_id][1] = core_distance
                if (not self.results_order.count(current_point_id)):
                    self.results_order.append(current_point_id)
                if core_distance < np.inf:
                    self.printer("节点{}为核心点，递归处理其邻域".format(point_id))
                    self._update(order_seeds, neighbors, current_point_id)

    def fit(self, points):
        """聚类主函数
        聚类过程主要是通过expand_cluste_order函数实现，流程如下：
        给定一个起始点pt，计算pt的core_distance和eps-邻域，并更新eps-邻域中数据点的
        reachability_distance
        然后按reachability_distance从小到大依次处理pt的eps-邻域中未处理的点（流程同上）

        遍历整个数据集，对每个未expand的数据点都执行expand，便完成了聚类，结果存储在self.results中
        数据点遍历顺序存储在self.results_order中，二者结合便可以导出具体的聚类信息

        :param points: [list] 输入数据列表，list中的每个元素都是长度固定的1维np数组
        :returns:
        :rtype:

        """
        """
        results[遍历标记，核心距离，可达距离]
        results_order 存放数据遍历顺序
        """

        self.point_num = len(points)
        self.point_size = points[0].size
        self.results = [[None, np.inf, np.inf] for x in range(self.point_num)]
        self.results_order = []
        ## 数据存储在kd树中以便检索【好像并没有用到检索...】
        self.kd_tree = KDTree(self.point_size)
        self.kd_tree.create(points)

        for point_id in range(self.point_num):
            ## 如果当前节点没有处理过，执行expand
            if not self.results[point_id][0]:
                self._expand_cluste_order(point_id)
        return self

    def extract(self, eps):
        """从计算结果中抽取出聚类信息
        抽取的方式比较简单，就是扫描所有数据点，判断当前点的core_distance
        和reachability_distance与给定eps的大小，然后决定点的类别。规则如下：
        1. 如果reachability_distance<eps，属于当前类别
        2. 如果大于eps，不属于当前类别
           2-1. 如果core_distance小于eps，可以自成一类
           2-2. 如果core_distance大于eps，认为是噪声点
        注意：
        数据的扫描顺序同fit函数中的处理顺序是一致的。
        :returns:
        :rtype:

        """
        if eps > self.max_eps:
            raise ValueError("eps参数不能大于{}，当前值为{}".format(self.max_eps, eps))
        labels = np.zeros(self.point_num, dtype=np.int64)
        counter = count()
        idx = next(counter)
        for point_id in self.results_order:
            # for point_id in range(self.point_num):
            _, core_distance, reachability_distance = self.results[point_id]
            ## 如果可达距离大于eps，认为要么是core point要么是噪音数据
            if reachability_distance > eps:
                ## 如果core distance小于eps，那么可以成为一个类
                if core_distance < eps:
                    idx = next(counter)
                    labels[point_id] = idx
                ## 否则成为噪声数据
                else:
                    labels[point_id] = 0
            ## 可达距离小于eps，属于当前类别
            ## 这个点的顺序是由fit函数中的主循环函数维持的，注意
            else:
                labels[point_id] = idx

        return labels


def extract_postprocess(labels):
    clusters = defaultdict(list)
    for ii in range(len(labels)):
        idx = str(labels[ii])
        clusters[idx].append(ii)
    return clusters


###############################################################
if __name__ == "__main__":

    def generate_test_data(n_samples=1000):
        """生成测试数据

        :param n_samples:
        :returns:
        :rtype:

        """
        # varied
        data = datasets.make_blobs(
            n_samples=n_samples, cluster_std=[1.0, 2.5, 0.5])

        # # noisy_circles
        # data = datasets.make_circles(n_samples=n_samples, factor=.5, noise=.05)

        # # noisy_moons
        # data = datasets.make_moons(n_samples=n_samples, noise=.05)

        # # blob
        # data = datasets.make_blobs(n_samples=n_samples, random_state=8)

        return data

    def hierarchical_dataset():
        cluster_1 = [3 * np.random.rand(2) for x in range(100)]
        cluster_2 = [0.5 + np.random.rand(2) / 1.2 for x in range(200)]
        cluster_3 = [0.5 + np.random.rand(2) / 4 for x in range(200)]
        cluster_4 = [2 + np.random.rand(2) / 3 for x in range(100)]
        cluster_5 = [
            np.array([0, 5]) + np.random.rand(2) * 1.3 for x in range(100)
        ]
        cluster_6 = [5 + np.random.randn(2) / 5 for x in range(200)]
        cluster_7 = [5 + np.random.randn(2) for x in range(100)]
        data = cluster_1 + cluster_2 + cluster_3 + cluster_4 + cluster_5 + cluster_6 + cluster_7
        return data

    def scatter(data, labels=None):
        """画散点图

        :param data: [list|np.array] 1维np数组构成的列表或两维np数组,第1和第2列分别表示横纵坐标
        :param label: [list|np.array|None] 数据点属于的类别，长度与data相同
        :returns:
        :rtype:

        """
        data = np.array(data)
        if labels is not None:
            plt.scatter(data[:, 0], data[:, 1], c=np.array(labels))
        else:
            plt.scatter(data[:, 0], data[:, 1])
        plt.show()

    def test_optics():

        # data, _ = generate_test_data(10000)
        # data = [data[i, :] for i in range(data.shape[0])]

        # data = hierarchical_dataset()
        X= pad.read_excel(r'D:\mmm\python\轨迹测试数据\1109-聚类\湘11_100015_2017-12-9_深松-BL.xls')
        data = StandardScaler().fit_transform(X)  # 通过去除均值并缩放到单位方差来标准化特征.适合数据，然后对其进行转换

        optics = OPTICS(
            max_eps=6, min_samples=4, metric=euclidean,
            verbose=False).fit(data)

        ## 从结果中提取出reachability_distance，按照数据处理顺序排列

        reachability_distance = np.array(
            [optics.results[i][2] for i in optics.results_order])

        ## 从结果中生成一个聚类

        eps = 6
        optics_labels = optics.extract(eps)

        color_nums = len(set(optics_labels))
        color_types = cm.rainbow(np.linspace(0, 1, color_nums))
        temp = [optics_labels[i] for i in optics.results_order]
        colors = [color_types[i] for i in temp]

        plot_data = np.array(data)

        plt.subplot(1, 2, 1)
        plt.scatter(
            plot_data[:, 0], plot_data[:, 1], c=np.array(optics_labels))

        plt.subplot(1, 2, 2)
        plt.bar(
            np.arange(0, optics.point_num),
            np.array(reachability_distance),
            width=3,
            color=colors)
        plt.show()

    def optics_vs_dbscan_2d():

        cluster_1 = [3 * np.random.rand(2) for x in range(100)]
        cluster_2 = [0.5 + np.random.rand(2) / 1.2 for x in range(200)]
        cluster_3 = [0.5 + np.random.rand(2) / 4 for x in range(200)]
        cluster_4 = [2 + np.random.rand(2) / 3 for x in range(100)]
        cluster_5 = [
            np.array([0, 5]) + np.random.rand(2) * 1.3 for x in range(100)
        ]
        cluster_6 = [5 + np.random.randn(2) / 5 for x in range(200)]
        cluster_7 = [5 + np.random.randn(2) for x in range(100)]

        cluster_2 = [3 + np.random.standard_exponential(2) for x in range(100)]
        cluster_3 = [-3 + np.random.rand(2) for x in range(300)]
        cluster_4 = [(-3 + np.random.rand(2)) * 3 for x in range(100)]
        data = cluster_1 + cluster_2 + cluster_3 + cluster_4
        # scatter(data)

        ## OPTICS
        optics = OPTICS(
            max_eps=10, min_samples=10, metric=euclidean,
            verbose=False).fit(data)
        eps = 1
        optics_labels = optics.extract(eps)

        ## DBSCAN
        array_data = np.array(data)
        db = DBSCAN(
            eps=eps, min_samples=10, metric=euclidean,
            n_jobs=-1).fit(array_data)

        db_labels = db.labels_

        ## plot
        plt.subplot(1, 2, 1)
        plt.scatter(
            array_data[:, 0], array_data[:, 1], c=np.array(optics_labels))
        plt.title("OPTICS")
        plt.subplot(1, 2, 2)
        plt.scatter(array_data[:, 0], array_data[:, 1], c=np.array(db_labels))
        plt.title("DBSCAN")
        plt.show()


    test_optics()