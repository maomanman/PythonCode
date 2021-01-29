# import matplotlib.pyplot as plt  # plt 用于显示图片
# import matplotlib.image as mpimg  # mpimg 用于读取图片
# from scipy import misc  # 用于图片缩放
# import numpy as np
# import os
# import tkinter.messagebox
# from tkinter.filedialog import *
#
# import re
#
# img = mpimg.imread(r'D:\精准农业部事务\学生照片收集-精准农业部\陈进-15676177615 - 副本.jpg')  # 读取和代码处于同一目录下的 lena.png
# # 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
# x, y, t = img.shape
#
# if x >= y:
#     bei = x / 640
#     x1 = 640
#     y1 = y / bei
#
# print(x, y, bei)
#
# img_sz = misc.imresize(img, (x1, y1, t))
# print(img_sz.shape)
# # plt.imshow(lena)  # 显示图片
# # plt.axis('off')  # 不显示坐标轴
# # plt.show()
#
#
# # root = Tk()
# # root.title('修改图片尺寸')
# # root.geometry("400x200")
# # # label1 = Label(root, text='原文件类型', height=1, width=20, fg="black")
# # # label1.pack(pady=10)
# # label2 = Label(root, text='', height=1, width=20, fg="black")
# # label2.pack()
# # btn1 = Button(root, text='选择需要修改的图片', command=changeFile)
# # btn1.pack(pady=20)
# # btn2 = Button(root, text='选择需要转换excel文件', command=lambda:changeFile(2))
# # btn2.pack(pady=10)




#coding=utf-8
import os  #打开文件时需要
from PIL import Image
import re

# Start_path=r'D:\精准农业部事务\学生照片收集-精准农业部\'
iphone5_width=640
iphone5_depth=640
# list=os.listdir(Start_path)
#print list
# count=0
# for pic in list:
#     path=Start_path+pic
#     print(path)
path=r'D:\精准农业部事务\学生照片收集-精准农业部\魏传省-13261819531.png'
im=Image.open(path)
w,h=im.size
    #print w,h
    #iphone 5的分辨率为1136*640，如果图片分辨率超过这个值，进行图片的等比例压缩
print(im.size)
if w>h and w>640:
#     print pic
#     print "图片名称为"+pic+"图片被修改"
    h_new=int(iphone5_width*h/w)
    w_new=iphone5_width
if h>=w and h>640:
#     print pic
#     print "图片名称为"+pic+"图片被修改"
    w_new=int(iphone5_depth*w/h)
    h_new=iphone5_depth
#     count=count+1
print(w_new,h_new)
out = im.resize((w_new,h_new),Image.ANTIALIAS)
print(out.size)

temp=path.split('.')
new_path=temp[0]+'-2.'+temp[1]
print(new_path)
out.save(new_path)
#
# if h>iphone5_depth:
#     print pic
#     print "图片名称为"+pic+"图片被修改"
#     w=iphone5_depth*w/h
#     h=iphone5_depth
#     count=count+1
#     out = im.resize((w_new,h_new),Image.ANTIALIAS)
#     new_pic=re.sub(pic[:-4],pic[:-4]+'_new',pic)
#     #print new_pic
#     new_path=Start_path+new_pic
#     out.save(new_path)

