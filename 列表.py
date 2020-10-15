"""
列表可修改的有序类型

索引号从 0 开始

列表是有序的

使用中括号 [] 表示列表
"""
"""
小技巧：
pycharm有自动调整代码格式的快捷键，默认为Alt+Ctrl+L，按下快捷键后，代码自动填充了空格。
"""

# #############创建列表
# names = ['张三', '李四', '王五']
# print(names)
#
# xingming = ('zhang', 'shao', 'lisi')
# names2 = list(xingming)  # list(可迭代对象)，可迭代对象一般用元组
# print(names2)
#
# print('错误演示', end=':')
# names_err = list('张三')  # 会将字符串进行分给成单个字符
# print(names_err)
#
# heros = ['ddd', 'ccc', 'eee', 'ttt']
# print('\n初始列表：{}'.format(heros))
# # ###########增加元素
# heros.append('aaa')  # 在列表最后插入
# print('append(\'aaa\') 在列表最后添加"aaa"：{}'.format(heros))  # ['ddd', 'ccc', 'eee', 'ttt', 'aaa']
#
# heros.insert(2, 'bbb')  # 在指定位置插入数据
# print('insert(2, \'bbb\') 在索引号为2的位置添加元素"bbb"：{}'.format(heros))  # ['ddd', 'ccc', 'bbb', 'eee', 'ttt', 'aaa']
#
# x = ('111', '2222', '3333')  # 可以是元组，也可以是列表
# heros.extend(x)  # x 是可迭代对象，extend 是在原列表后拼接新的一串数据
# print('heros.extend(x) 将元组x{}拼接到列表后：{}'.format(x,
#                                                heros))  # ['ddd', 'ccc', 'bbb', 'eee', 'ttt', 'aaa', '111', '2222', '3333']
#
# # ########删除
# heros.pop()  # 默认删除列表最后一个元素
# print('pop()默认删除列表后的最后一个元素：{}'.format(heros))
#
# heros.pop(0)  # 删除指定位置的元素 0-指定第一个位置元素被删除
# print('pop(0)删除索引号为0的元素：{}'.format(heros))
#
# heros.remove("111")  # 删除指定元素
# print('remove("111")删除元素"111"：{}'.format(heros))
#
# # heros.clear()  # 删除所有元素
# # print(heros)
#
# # del heros #将整个变量都删除，后续就没有这个变量了
# # print(heros) #del 后再打印就会报备没有定义这个变量
#
# del heros[2]  # 也可以删除列表中指定的位置
# print('del heros[2] 删除索引号为2的数：{}'.format(heros))
#
# # ###########查询
#
# print('index("2222") 查询元素“2222”的索引号：{}'.format(heros.index("2222")))  # 待查询的元素不存在会报错
#
# print('count("2222") 查询元素“2222”的个数：{}'.format(heros.count("2222")))  # 待查询的元素不存在会报错
#
# # in 运算符
# print('aaa' in heros)
#
# # ##########修改
# # 直接通过下标进行修改
#
# # # 遍历
# # print('for循环')
# # for h in heros:
# #     print(h)
# #
# # print('\nwhile循环')
# # i = 0
# # while i < len(heros):
# #     print(heros[i])
# #     i += 1
#
# # 排序
# # nums = [2, 3, 0, 6, 1, 2, 9, 5, 3]
# # print('原始列表nums={}'.format(nums), end=' ')
# # nums.sort()
# heros.sort()
# print('sort() 排序后{}'.format(heros))
#
# # y = sorted(heros)
# # print('sorted(heros)排序后：{}'.format(y))
#
# # 逆序,反转
# heros.reverse()
# print("reverse() 是将原列表顺序反转： {}".format(heros))
#
# # 列表的复制
#
# x = heros.copy()
# print("x 是heros的复制体,用列表的copy方法，不同的内存 {}".format(x))
#
# import copy
#
# y = copy.copy(heros)
# print("y 是heros的复制体,用模块的copy方法，不同的内存 {}".format(y))

import random

nums = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
rooms = [[], [], []]

for num in nums:
    room = random.choice(rooms)  # 随机选择第二层列表
    room.append(num)

print(rooms)

for i, room in enumerate(rooms): # 此处用in对元素进行遍历，用了enumerate类后可在遍历元素的同时获取下标号
    print("第%d个房间有%d个人：{}".format(room) % (i, len(room)))


