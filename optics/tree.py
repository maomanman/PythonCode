"""
定义了二叉树的基本操作
"""
# -*- coding: utf-8 -*-

class Node:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    @property
    def is_leaf(self):
        """如果没有左右子节点,就是叶子节点

        :returns:
        :rtype:

        """

        return (not self.left) and (not self.right)

    def preorder(self):
        """先序遍历递归版本
        遍历顺序为root->left->right
        :returns:
        :rtype:

        """

        if not self:
            return

        yield self

        if self.left:
            for x in self.left.preorder():
                yield x

        if self.right:
            for x in self.right.preorder():
                yield x

    def preorder_norecur(self):
        """先序遍历非递归版本
        遍历顺序为root->left->right
        :returns:
        :rtype:

        """

        if not self:
            return
        stack = [self]
        while stack:
            node = stack.pop()
            yield node
            ## 后入先出
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

    def inorder(self):
        """中序遍历递归版本
        遍历顺序为left->root->right
        :returns:
        :rtype:

        """
        if not self:
            return

        if self.left:
            for x in self.left.inorder():
                yield x

        yield self

        if self.right:
            for x in self.right.inorder():
                yield x

    def inorder_norecur(self):
        """中序遍历非递归版本
        遍历顺序为left->root->right

        :returns:
        :rtype:
        中序遍历的思路是先一直找到最左子节点,把沿途所有节点都入栈,
        然后开始出栈,出栈之后把当前节点设置为上一个节点的右子节点,
        进行右子树的遍历(如果右子树为空显然就免于遍历了)

        """

        if not self:
            return

        stack = []

        node = self

        while node is not None or len(stack) > 0:
            if node is not None:
                stack.append(node)
                node = node.left
            else:
                # 如果node是叶子节点,那么node.right==None,下次会继续弹出node的父节点
                # 如果node不是叶子节点,且node.right非空,那么下次会执行入栈操作
                node = stack.pop()
                yield node
                node = node.right

    def postorder(self):
        """后序遍历递归版本
        遍历顺序为left->right->root

        :returns:
        :rtype:

        """

        if not self:
            return

        if self.left:
            for x in self.left.postorder():
                yield x

        if self.right:
            for x in self.right.postorder():
                yield x

        yield self

    def postorder_norecur(self):
        """后序遍历非递归版本
        遍历顺序为left->right->root
        和中序遍历不同的是,只有下面两种情况之一才能出栈:
        1. 栈顶元素为叶子节点,此时肯定可以出栈,否则没有节点可以入栈了
        2. 栈顶元素不是叶子节点,但是上一个出栈的元素是栈顶元素的右子节点
           上一个出栈的元素是栈顶元素的右子节点说明节点的右子数已经遍历过了,
           所以现在当前节点可以出栈了

        :returns:
        :rtype:

        """

        if not self:
            return

        stack = []

        node = self
        last_node = None
        while node is not None or len(stack) > 0:
            if node is not None:
                stack.append(node)
                node = node.left
            else:
                # 这里不会越界,因为能进到这里的前提条件是node is None
                # 这时必然有stack非空,否则while循环就退出了
                temp = stack[-1]
                if temp.is_leaf or temp.right is last_node:
                    node = stack.pop()
                    last_node = node
                    yield node
                    # 这里node要设置为None,因为该节点及左右子树都已遍历,需要向上回溯了
                    # 注意中序遍历时这里设置的是node=node.right,因为右子树实在父节点
                    # 遍历后才遍历的
                    node = None
                else:
                    node = temp.right

    def breadth_frist(self):
        """广度优先遍历
        和深度优先遍历(前/中/后序遍历)的区别是使用队列而不是栈.
        :returns:
        :rtype:

        """

        if not self:
            return

        queue = [self]
        while queue:
            node = queue.pop(0)  # 弹出队列首个元素,若直接调用list.pop()则弹出末尾元素
            yield node
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)


    @property
    def children(self):
        """
        Returns an iterator for the non-empty children of the Node

        The children are returned as (Node, pos) tuples where pos is 0 for the
        left subnode and 1 for the right.

        >>> len(list(create(dimensions=2).children))
        0

        >>> len(list(create([ (1, 2) ]).children))
        0

        >>> len(list(create([ (2, 2), (2, 1), (2, 3) ]).children))
        2
        """

        if self.left and self.left.data is not None:
            yield self.left, 0
        if self.right and self.right.data is not None:
            yield self.right, 1

    def set_child(self, index, child):
        """ Sets one of the node's children

        index 0 refers to the left, 1 to the right child """

        if index == 0:
            self.left = child
        else:
            self.right = child

    def height(self):

        min_height = int(bool(self))
        return max([min_height] + [c.height() + 1 for c, p in self.children])

    def __repr__(self):
        return '<%(cls)s - %(data)s>' % \
            dict(cls=self.__class__.__name__, data=repr(self.data))

    # def __nonzero__(self):
    #     return self.data is not None

    # __bool__ = __nonzero__

    # def __eq__(self, other):
    #     if isinstance(other, tuple):
    #         return self.data == other
    #     else:
    #         return self.data == other.data

    def __hash__(self):
        return id(self)