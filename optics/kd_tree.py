"""
KD树
"""
# -*- coding: utf-8 -*-

import numpy as np
from scipy.spatial.distance import euclidean
from tree import Node


class KDNode(Node):
    def __init__(self,
                 data=None,
                 left=None,
                 right=None,
                 axis=None):
        super(KDNode, self).__init__(data, left, right)
        self.axis = axis


class KDTree:
    """
    KD树的实现。
    注意树结构中，输入数据会被原样保存在points成员中，node.data存储的是数据在points中的位置
    索引，相当于保存了指针。
    """
    def __init__(self, dimension, dist_func=euclidean, leaf_size=5):
        """初始化

        :param dimension:
        :param dist_func:
        :param leaf_size:
        :returns:
        :rtype:

        """
        self.dimension = dimension
        self.root = None
        self.dist_func = dist_func
        self.leaf_size = leaf_size

    def _next_axis(self, current_axis):
        return (current_axis + 1) % self.dimension

    def _create(self, handles, current_axis):
        if len(handles) <= self.leaf_size:
            return KDNode(handles, None, None, None)
        ## handle排序要用到真实的数据
        handles.sort(key=lambda x: self.points[x][current_axis])
        median = len(handles) // 2
        data = [handles[median]]  # 数据点是list格式，存储handle
        left = self._create(handles[:median], self._next_axis(current_axis))
        right = self._create(handles[median + 1:],
                             self._next_axis(current_axis))

        return KDNode(data, left, right, axis=current_axis)

    def __getitem__(self,key):
        return self.points[key]

    def height(self):
        if self.root:
            return self.root.height()
        else:
            raise ValueError("KD树尚未构建")



    def create(self, points):
        self.points=points
        handles=list(range(len(points)))
        self.root = self._create(handles, 0)
        self.maxes = np.amax(self.points,axis=0)
        self.mins = np.amin(self.points,axis=0)


    def router(self, root, point):
        """给定一个点,找到它属于的叶子节点,返回从root到叶子节点路径上的所有节点

        :param root: 根节点
        :param point: 指定点
        :returns:
        :rtype:

        """
        results = [root]
        node = root
        while not node.is_leaf:
            if point[node.axis] < self.points[node.data[0]][node.axis]:
                node = node.left
            else:
                node = node.right
            results.append(node)
        return results

    def find_nn(self, node, point, k):
        """计算node数据中与point最近的k个点
        这里采用的方式是逐个计算然后排序,比较慢
        :param node: KD树的某个节点
        :param point: 待比较数据点
        :param k:
        :returns:
        :rtype:

        """
        dists = [self.dist_func(self.points[x], point) for x in node.data]
        idx = np.argsort(dists)[:k]
        # return [(dists[i],self.points[node.data[i]]) for i in idx]
        return [(dists[i],node.data[i]) for i in idx]

    def check_intersection(self, node, point, radius):
        """检查node对应的的切分超平面是否与(point,radius)定义的超球体相交
        NOTE:如果不是欧式距离,会不会对相交的判断有影响?

        :param node: KD树的某个节点
        :param point: 球心
        :param radius: 球半径
        :returns:
        :rtype:

        """
        if node.is_leaf:
            raise ValueError("节点不能是叶子节点!")
        point_2 = point.copy()
        point_2[node.axis] = self.points[node.data[0]][node.axis]
        dist = self.dist_func(point, point_2)
        return True if dist < radius else False

    def knn(self, point, k=1, verbose=True):
        """利用kd树寻找knn
        实现方法有点类似树的后序遍历,区别在于这里有些子节点不需要遍历,而且遍历顺序是不固定的.
        对每个访问过的节点都标记成已访问

        :param point: 输入数据点
        :param k: 返回最近邻的数据
        :param verbose: 为True表示会输出详细处理信息
        :returns: k近邻搜索结果，注意返回的是数据在kd树中的id而非数据点本身
        :rtype: list of tuple(distance,point_id)

        """

        if verbose:
            vprint = print
        else:
            vprint = lambda x: None
        if not self.root:
            raise ValueError("KD树尚未构建...")
        # 初始化
        for node in self.root.preorder_norecur():
            node.visited = None
        vistied_points = 0
        # results = [(None, -np.inf)] * k
        results = [(np.inf, None)] * k
        ## 也可以用堆来实现nn的更新
        # heapq.heapify(results)
        vprint("初始化节点栈为树根节点")
        path = self.router(self.root,point)
        while path:
            node = path.pop()
            node.visited = True
            vistied_points += len(node.data)
            vprint("{}更新结果集".format(" " * 4))
            neighbors=self.find_nn(node, point, k)
            results.extend(neighbors)
            results.sort(key=lambda x: x[0])
            results = results[:k]

            # for neighbor in neighbors:
            #     heapq.heappushpop(results,neighbor)

            if len(path) == 0:
                vprint("搜索结束,一共搜索了{}个数据点".format(vistied_points))
                return results
                # sorted_results = heapq.nlargest(k,results)
                # return [(x[0],x[1]) for x in sorted_results]
            parent = path[-1]
            vprint("{}判断节点的切分平面是否与超球体相交".format(" " * 4))
            # radius = results[-1][1]
            radius = results[-1][0]
            if self.check_intersection(parent, point, radius):
                vprint("{}相交,另一个子节点加入处理栈".format(" " * 8))
                other_node = parent.left if parent.right is node else parent.right
                # 如果没访问过,就访问,否则回溯到父节点
                if not other_node.visited:
                    path.extend(self.router(other_node,point))
            vprint("剩余节点数:{}".format(len(path)))



    def _min_dist(self,maxes,mins,point):
        return self.dist_func(point*0, np.maximum(0,np.maximum(mins-point,point-maxes)))

    def _max_dist(self,maxes,mins,point):
        return self.dist_func(point*0, np.maximum(maxes-point,point-mins))

    ## 寻找距离点x小于r的所有点
    def query_ball_point(self, point, r):
        stack=[(self.root,self.maxes,self.mins)]
        results=[]
        while stack:
            node,maxes,mins=stack.pop()
            # 如果是叶子节点，检查节点保存的数据是否满足即可
            if node.is_leaf:
                for handle in node.data:
                    distance=self.dist_func(self.points[handle],point)
                    if distance<=r:
                        results.append((distance,handle))

            # 如果矩形内所有点距离都大于r，不用检查
            elif self._min_dist(maxes,mins,point) > r:
                continue

            # 如果矩形内所有点距离都小于r，遍历，把所有节点都返回
            elif self._max_dist(maxes,mins,point) < r :
                for sub_node in node.preorder_norecur():
                    for handle in sub_node.data:
                        distance=self.dist_func(self.points[handle],point)
                        results.append((distance,handle))

            # 如果都不满足，拆成子矩形，继续检查
            else:
                # 先判断将当前节点的数据是否满足条件
                handle = node.data[0]
                distance=self.dist_func(self.points[handle],point)
                if distance<=r:
                    results.append((distance,handle))

                # 改变左子节点的最大值和右子节点的最小值
                left_maxes=maxes.copy()
                left_maxes[node.axis]=self.points[node.data[0]][node.axis]

                right_mins=mins.copy()
                right_mins[node.axis]=self.points[node.data[0]][node.axis]

                # 入栈
                stack.append((node.left,left_maxes,mins))
                stack.append((node.right,maxes,right_mins))
        results.sort(key=lambda x:x[0] )
        return results

if __name__=="__main__":

    def knn_direct(points, point, k, dist_func=euclidean):
        dists = [dist_func(x, point) for x in points]
        idx = np.argsort(dists)[:k]
        return [( dists[i],i) for i in idx]

    def query_ball_point_direct(points, input_point, r, dist_func=euclidean):
        results=[]
        for ii in range(len(points)):
            distance=dist_func(points[ii],input_point)
            if distance<=r:
                results.append((distance,ii))
        results.sort(key=lambda x:x[0] )
        return results


    ##### test #####


    def test_knn(dim=3, point_num=5000, k=10, verbose=False):

        points = [np.random.rand(dim) for ii in range(point_num)]

        input_point = np.random.rand(dim)

        kd_tree = KDTree(dimension=dim,leaf_size=10)
        kd_tree.create(points)


        kd_tree_result = kd_tree.knn(input_point, k, verbose=verbose)
        kd_tree_result_points=[kd_tree[x[1]] for x in kd_tree_result]
        kd_tree_result_distance = [x[0] for x in kd_tree_result]

        direct_result=knn_direct(points, input_point, k, dist_func=euclidean)
        direct_result_points=[points[x[1]] for x in direct_result]
        direct_result_distance = [x[0] for x in direct_result]

        distance_result = np.array_equal(kd_tree_result_distance, direct_result_distance)
        points_result = np.array_equal(kd_tree_result_points, direct_result_points)
        if not distance_result :
            print("距离计算错误！")
        elif not points_result:
            print("数据点计算错误！")
        else:
            print("测试通过!!!!!")

    def test_query(dim=3, point_num=5000, r=0.2, verbose=False):

        points = [np.random.rand(dim) for ii in range(point_num)]

        input_point = np.random.rand(dim)

        kd_tree = KDTree(dimension=dim,leaf_size=10)
        kd_tree.create(points)


        kd_tree_result=kd_tree.query_ball_point(input_point,r)
        kd_tree_result_points=[kd_tree[x[1]] for x in kd_tree_result]
        kd_tree_result_distance = [x[0] for x in kd_tree_result]

        direct_result = query_ball_point_direct(points, input_point, r, dist_func=euclidean)
        direct_result_points=[points[x[1]] for x in direct_result]
        direct_result_distance = [x[0] for x in direct_result]

        distance_result = np.array_equal(kd_tree_result_distance, direct_result_distance)
        points_result = np.array_equal(kd_tree_result_points, direct_result_points)
        if not distance_result :
            print("距离计算错误！")
        elif not points_result:
            print("数据点计算错误！")
        else:
            print("测试通过!!")


    def test_traversal(dim=3, point_num=20, traversal_type="postorder"):
        if traversal_type not in ["preorder", "inorder", "postorder"]:
            raise ValueError(
                "traversal_type \"{}\" not recognized".format(traversal_type))

        points = [np.random.rand(dim) for ii in range(point_num)]

        kd_tree = KDTree(dimension=dim)
        kd_tree.create(points)

        if traversal_type == "preorder":
            traversal_iter = zip(kd_tree.root.preorder(),
                                 kd_tree.root.preorder_norecur())
        elif traversal_type == "inorder":
            traversal_iter = zip(kd_tree.root.inorder(),
                                 kd_tree.root.inorder_norecur())
        elif traversal_type == "postorder":
            traversal_iter = zip(kd_tree.root.postorder(),
                                 kd_tree.root.postorder_norecur())

        for ii, jj in traversal_iter:
            if ii is jj:
                print("OK")
            else:
                print("BAD")