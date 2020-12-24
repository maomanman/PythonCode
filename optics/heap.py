"""
最小堆
"""
# -*- coding: utf-8 -*-
#
from verbose import Verbose

class Heap(Verbose):
    """
    最小堆，同时可直接用作优先队列

    """

    def __init__(self, verbose=True):
        """初始化
        heap成员存储的元素是[key,handle]形式的list
        handle_dict存放handle和heap位置的对应关系，用于快速检索元素在heap中的下标
        具体的数据可以存放在外部，只要与handle_dict的key一一对应即可
        :returns:
        :rtype:

        """
        self.heap = []  #
        self.handle_dict = {}  #
        super(Heap, self).__init__(verbose)

    def _siftup(self, pos):
        """维护最小堆结构，即算法导论中的max-heapify函数
        思路：
        假设pos的左右子节点均已经是最小堆，但是pos位置的值可能大于其左右子节点值，
        所以要找到更小的子节点（childpos），然后交换根节点（pos）和最小子节点的值。
        这样以来，对应子节点的最小堆性质可能会被破坏，所以要在子节点上执行同样的操
        作，这样一直递归地走下去直到达到叶子节点。
        时间复杂度为O(logN)
        :param pos:
        :returns:
        :rtype:

        """

        end_pos = len(self.heap)
        lchild = 2 * pos + 1
        rchild = lchild + 1

        # 最小节点设置为左子节点
        min_pos = lchild
        # 若左子节点都不小于end_pos,说明pos肯定是叶子节点了
        while min_pos < end_pos:
            if self.heap[min_pos] > self.heap[pos]:
                min_pos = pos
            if rchild < end_pos and self.heap[min_pos] > self.heap[rchild]:
                min_pos = rchild
            if min_pos != pos:
                ## 不满足最小堆性质，进行交换
                self.printer("交换位置{}:{}和{}:{}的数据".format(
                    min_pos, self.heap[min_pos], pos, self.heap[pos]))
                self.printer("交换位置{}和{}的数据".format(min_pos, pos))
                self.heap[min_pos], self.heap[pos] = self.heap[pos], self.heap[
                    min_pos]
                self.printer("更新handle_dict")
                self.printer("{}->{}".format(self.heap[pos][1], min_pos))
                self.printer("{}->{}".format(self.heap[min_pos][1], pos))
                self.handle_dict[self.heap[pos][1]] = pos
                self.handle_dict[self.heap[min_pos][1]] = min_pos
                pos = min_pos
                lchild = 2 * pos + 1
                rchild = lchild + 1
                min_pos = lchild
            else:
                # 满足最小堆性质，不用处理
                break

    def _siftdown(self, pos):
        """当一个节点（pos）值变小时，为了保持最小堆性质，需要将该值往上浮动，
        具体做法就是不断交换节点值和父节点值，类似冒泡排序。
        注意：
        1. 减小节点的值不会影响子节点的最小堆性质
        2. 交换该节点和其父节点的值也不会影响该节点的子节点的最小堆性质，因为
           父节点的值肯定小于该节点的两个子节点
        时间复杂度为O(logN)
        :param startpos:
        :param pos:
        :returns:
        :rtype:

        """
        new_item = self.heap[pos]
        while pos > 0:
            parentpos = (pos - 1) >> 1
            parent_item = self.heap[parentpos]
            # 如果当前节点值小于父节点值，上浮
            if new_item < parent_item:  # list之间的比较是比较其第一个元素，即key
                self.heap[pos] = parent_item
                self.handle_dict[parent_item[1]] = pos  # 更新handle_dict位置信息
                pos = parentpos
                continue
            # 一旦发现不小于了，就结束，把原来pos位置的值（new_item）放在这里
            break
        self.heap[pos] = new_item
        self.handle_dict[new_item[1]] = pos

    def heapify(self, x):
        """建堆
        时间复杂度为O(N)
        :param x: [list] 输入数据，格式为[[key,handle]..]
        :returns:
        :rtype:

        """
        n = len(x)
        self.heap = x
        for i in range(n):
            self.handle_dict[x[i][1]] = i
        ## 只有前半部分数据才能成为根节点
        for i in reversed(range(n // 2)):
            self._siftup(i)

    def push(self, data):
        """添加一个元素
        时间复杂度为O(logN)
        :param data:
        :returns:
        :rtype:

        """
        key, handle = data
        try:
            # 已经存在，增加或者减小key
            pos = self.handle_dict[handle]
            if self.heap[pos][0] > key:
                self.decrease_key(data)
            elif self.heap[pos][0] < key:
                self.increase_key(data)
        except:
            # 不存在，添加之，具体做法是将元素添加到heap的最后面，作为叶子节点
            # 然后逐渐上浮
            self.heap.append(data)
            self.handle_dict[handle] = len(self.heap) - 1
            self._siftdown(len(self.heap) - 1)

    def decrease_key(self, data):
        """减小某个元素的key
        减小key时，当前节点及子节点的最小堆性质肯定会留存，所以不需要再维护最小堆
        性质，只需要当前元素往上浮即可
        时间复杂度为O(logN)
        :param data:
        :returns:
        :rtype:

        """
        new_key, handle = data
        pos = self.handle_dict[handle]
        if self.heap[pos][0] < new_key:
            raise ValueError("新的key比原有key更大")
        self.heap[pos][0] = new_key
        self._siftdown(pos)

    def increase_key(self, data):
        """增加某个元素的key，和decrease_key类似
        时间复杂度为O(logN)
        :param data:
        :returns:
        :rtype:

        """
        new_key, handle = data
        pos = self.handle_dict[handle]
        if self.heap[pos][0] > new_key:
            raise ValueError("新的key比原有key更小")
        self.heap[pos][0] = new_key
        self._siftup(pos)

    def pop(self):
        """弹出最小元素，保持小堆性质不变。
        具体方法如下（假设堆非空）：
        1. 弹出heap最后一个元素（last_item）
        2. 返回值设置为第一个元素（最小值）
        3. heap第一个元素设置为last_item
        4. 在第一个元素的位置上执行_siftup
        以上步骤可以避免直接弹出heap第一个元素后又要把最后一个元素移至首位的麻烦
        该方法也可以直接用于堆排序，但是要注意数据备份
        :returns:
        :rtype:

        """
        last_item = self.heap.pop()
        if self.heap:
            return_item = self.heap[0]
            self.heap[0] = last_item

            ## 更新handle_dict
            self.handle_dict[last_item[1]] = 0
            del self.handle_dict[return_item[1]]
            self._siftup(0)
        else:
            return_item = last_item
            del self.handle_dict[return_item[1]]
        return return_item

    def min(self):
        """返回堆的最小值
        时间复杂度为O(1)
        :returns: 堆中的最小元素
        :rtype: list

        """
        return self.heap[0]

    @property
    def is_empty(self):
        return True if len(self.heap) == 0 else False


if __name__=="__main__":
    import  numpy as np
    def build_heap(data_size):
        indices = list(range(data_size))
        keys = np.random.rand(data_size)
        handles = list(range(data_size))
        np.random.shuffle(handles)
        data = [list(x) for x in zip(keys, handles)]
        np.random.shuffle(indices)
        data = [data[idx] for idx in indices]
        zzs = Heap(verbose=False)
        zzs.heapify(data)
        return zzs


    def do_test(heap):
        data_size = len(heap.heap)

        reason = "通过！"
        for pos in range(data_size // 2):
            lchild = pos * 2 + 1
            rchild = lchild + 1
            if lchild < data_size and heap.heap[lchild] < heap.heap[pos]:
                reason = "失败：左子节点更小"
                break
            if rchild < data_size and heap.heap[rchild] < heap.heap[pos]:
                reason = "失败：右子节点更小"
                break
        for handle in heap.handle_dict:
            pos = heap.handle_dict[handle]
            if heap.heap[pos][1] != handle:
                reason = "建堆测试通过，但handle_dict记录不正确"
                break
        print(reason)


    def test_heapify(data_size=10):
        """测试建堆函数，同时也测试了_siftup函数

        :param data_size:
        :returns:
        :rtype:

        """
        zzs = build_heap(data_size)
        do_test(zzs)


    def test_siftdown(data_size=10):
        zzs=build_heap(data_size)
        pos=np.random.randint(data_size)
        zzs._siftdown(pos)
        ## 测试堆的性质是否能够保留
        print("测试1：不改变数据，直接调用")
        do_test(zzs)

        print("测试2：减小节点数据后再调用")
        zzs.heap[pos][0]=-np.inf
        zzs._siftdown(pos)
        do_test(zzs)

    def test_decrease_key(data_size=10):
        zzs=build_heap(data_size)
        pos=np.random.randint(data_size)
        zzs.decrease_key([-np.inf,pos])
        do_test(zzs)

    def test_increase_key(data_size=10):
        zzs=build_heap(data_size)
        pos=np.random.randint(data_size)
        zzs.increase_key([np.inf,pos])
        do_test(zzs)

    def test_push(data_size=10):
        zzs=build_heap(data_size)
        print("测试1：插入重名节点,值更小")
        pos=np.random.randint(data_size)
        new_data=zzs.heap[pos].copy()
        new_data[0]=new_data[0]-1
        zzs.push(new_data)
        do_test(zzs)
        print("测试2：插入重名节点,值更大")
        pos=np.random.randint(data_size)
        new_data=zzs.heap[pos].copy()
        new_data[0]=new_data[0]+1
        zzs.push(new_data)
        do_test(zzs)
        print("测试3：插入重名节点,值不变")
        pos=np.random.randint(data_size)
        new_data=zzs.heap[pos].copy()
        zzs.push(new_data)
        do_test(zzs)
        print("测试4：插入新节点")
        new_data=[np.inf,data_size]
        zzs.push(new_data)
        do_test(zzs)

    def test_pop(data_size=10):
        zzs=build_heap(data_size)
        pop_result=[]
        while zzs.heap:
            pop_result.append(zzs.pop())
            try:
                do_test(zzs)
            except:
                continue
        pop_result=[x[0] for x in pop_result]
        print(pop_result)