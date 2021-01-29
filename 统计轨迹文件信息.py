import os
import pandas as pd
import tkinter.messagebox as tkm
# from tkMessageBox import *
from tkinter.filedialog import *
import sys

import tkinter as tk

from tkinter import ttk
import re  # 用于字符串的多个分割符分割


class App:
    def __init__(self, root):
        # (1) 显示索引文件相关信息
        index_file_frame = tk.Frame(root)
        index_file_frame.place(x=0, y=0, width=600, height=80)
        label1 = tk.Label(index_file_frame, text='轨迹索引文件：')
        label1.place(x=0, y=0, width=100, height=40)
        self.index_file_entry = tk.Entry(index_file_frame)
        self.index_file_entry.place(x=100, y=10, width=350, height=20)
        self.index_file_button = tk.Button(index_file_frame, text='选择文件', command=self.selectFile)
        self.index_file_button.place(x=460, y=5, width=60, height=30)
        self.show_index_file_button = tk.Button(index_file_frame, text='读取文件', command=self.readIndexFile)
        self.show_index_file_button.place(x=525, y=5, width=60, height=30)
        label2 = tk.Label(index_file_frame, text='最大文件序号：')
        label2.place(x=0, y=30, width=100, height=40)
        self.max_file_index_entry = tk.Entry(index_file_frame)
        self.max_file_index_entry.place(x=100, y=40, width=50, height=20)
        label3 = tk.Label(index_file_frame, text='待处理文件序号：')
        label3.place(x=160, y=30, width=100, height=40)
        self.do1_file_index_entry = tk.Entry(index_file_frame)
        self.do1_file_index_entry.place(x=260, y=40, width=50, height=20)
        label4 = tk.Label(index_file_frame, text='——')
        label4.place(x=310, y=30, width=10, height=40)
        self.do2_file_index_entry = tk.Entry(index_file_frame)
        self.do2_file_index_entry.place(x=320, y=40, width=50, height=20)
        label5 = tk.Label(index_file_frame, text='（上限不能超过最大文件序号）', fg='red')
        label5.place(x=370, y=40, width=170, height=20)

        pathname = r'D:\mmm\轨迹数据集\轨迹索引-v1.0.xlsx'
        if os.path.exists(pathname):
            self.path = r'D:\mmm\轨迹数据集'
            self.index_data = pd.read_excel(pathname)
            self.index_file_entry.delete(0, END)
            self.index_file_entry.insert(0, pathname)
        else:
            self.index_file_entry.delete(0, END)

        # (2) 处理
        detail_file_frame = tk.Frame(root)
        detail_file_frame.place(x=0, y=80, width=600, height=30)
        get_work_time = tk.Button(detail_file_frame, text='计算工作时长', command=self.getWorkTime)
        get_work_time.place(x=190, y=0, width=100, height=30)
        get_filed_area = tk.Button(detail_file_frame, text='计算地块面积', command=self.getFiledArea)
        get_filed_area.place(x=310, y=0, width=100, height=30)

    def selectFile(self):
        # 打开文件路径，并选择索引文件
        f = askopenfilenames(title='选择索引文件', filetypes=[('*', 'xls'), ('*', 'xlsx')])
        if (f == '' or len(f) > 1):
            tkm.showwarning('警告', '只能选择一个文件')
        else:
            pathname = f[0]
            self.path = os.path.split(pathname)[0]
            self.index_data = pd.read_excel(pathname)
            self.index_file_entry.delete(0, END)
            self.index_file_entry.insert(0, pathname)

    def readIndexFile(self):
        # 读取索引文件信息，并显示
        max_index = int(self.index_data.文件序号.max())
        self.max_file_index_entry.delete(0, END)
        self.max_file_index_entry.insert(0, max_index)

    def getWorkTime(self):
        lowInedx = int(self.do1_file_index_entry.get())
        highIndex = int(self.do2_file_index_entry.get())
        workTimeInfo = pd.DataFrame(columns=['文件名称', '工作时长', '幅宽'])
        j = 0

        for fileIndex in range(lowInedx, highIndex + 1):
            name = self.path + '\\汇总\\' + self.index_data.loc[fileIndex, '文件名称']
            data = pd.read_excel(name)
            col = list(data.columns)
            for t, tag in enumerate(col):
                if tag.find('幅宽') != -1:
                    fukuan = tag
                    break
            count = data.shape[0]
            flag = 0  # 标识开始结束时间
            sumTime = pd.to_timedelta(0)
            for i in range(0, count - 1):  # range 包含 起点 不包含 终点
                if flag == 0:
                    startTime = data.loc[i, 'GPS时间']
                    # print('start：{}  {}'.format(data.loc[i, '序列号'],startTime))
                    flag = 1
                if data.loc[i + 1, '序列号'] - data.loc[i, '序列号'] == 1:  # 说明轨迹点不连续
                    if i == count - 2:
                        endTime = data.loc[i + 1, 'GPS时间']
                        # print('end：{} {}'.format(data.loc[i+1, '序列号'],endTime))
                    else:
                        continue
                else:
                    endTime = data.loc[i, 'GPS时间']
                    # print('end：{} {}'.format(data.loc[i, '序列号'],endTime))

                if type(startTime) == str:
                    startTime = pd.Timestamp(startTime)
                    endTime = pd.Timestamp(endTime)
                sumTime = sumTime + (endTime - startTime)
                flag = 0
            workTimeInfo.loc[j] = [self.index_data.loc[fileIndex, '文件名称'], sumTime,
                                   float(data.loc[:, fukuan].mode())]
            j = j + 1
            del data

        workTimeInfo.to_excel(self.path + '\\' + 'workTimeInfo'+'-'+str(lowInedx)+'-'+str(highIndex)+'.xlsx')

        tkm.showinfo('提示','工作时长已计算完毕！')

    def getFiledArea(self):
        pass


# 创建一个toplevel的根窗口，并把他作为擦参数实例化APP对象
root = tk.Tk()
root.title('根据序列号分割文件')
root.geometry("600x120+480+300")
app = App(root)
# 开始主事件循环
root.mainloop()
del app
del root
