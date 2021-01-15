import os
import pandas as pd
import tkinter.messagebox
from tkinter.filedialog import *

import re



def changeFile(flag=1):
    """
    转换文件：
    --------------------------------------
    flag  |
    --------------------------------------
     = 1  |   excel --> cvs  cvs: *-->utf-8
     = 2  |   cvs --> excel
    ----------------------------------------
    :return:
    """
    label2.config(text='')
    if flag == 1: #-->csv
        openTitle='选择excel或csv文件转换成utf-8编码的csv文件'
        selectFileTypes=[('*', 'xls'),('*','xlsx'),('*','csv')]
    elif flag ==2 : # -->excel
        openTitle = '选择csv文件转换excel文件'
        selectFileTypes = [('*','csv')]
    fn = askopenfilenames(title=openTitle, filetypes=selectFileTypes)
    if fn != '':
        for i in range(len(fn)):
            name = fn[i]
            if flag == 1: #-->csv
                if name.split('.')[1] == 'csv':
                    try:
                        data = pd.read_csv(name, encoding='ANSI')
                    except Exception as e:
                        continue
                elif name.split('.')[1] == 'xls' or name.split('.')[1] == 'xlsx':
                    data = pd.read_excel(name)
                else:
                    print("[{}]文件类型错误".format(name))
                    continue

                newName = name.split('.')[0] + '.csv'
                if '序列号' not in data.columns:
                    data.insert(0, '序列号', range(1, data.shape[0] + 1))

                data.set_index('序列号', inplace=True)
                data.to_csv(newName, encoding='utf-8')
            elif flag ==2 : # -->excel
                if name.split('.')[1] == 'csv' :
                    try:
                        data = pd.read_csv(name, encoding='ANSI')
                    except Exception as e:
                        data = pd.read_csv(name)
                else:
                    continue
                newName = name.split('.')[0] + '.xls'
                if '序列号' not in data.columns:
                    data.insert(0, '序列号', range(1, data.shape[0] + 1))
                data.set_index('序列号', inplace=True)
                data.to_excel(newName)
            del data
        label2.config(text='转换完成',fg='red')


root = Tk()
root.title('excel2cvs')
root.geometry("400x200")
# label1 = Label(root, text='原文件类型', height=1, width=20, fg="black")
# label1.pack(pady=10)
label2 = Label(root, text='', height=1, width=20, fg="black")
label2.pack()
btn1 = Button(root, text='选择需要转换成csv文件', command=changeFile)
btn1.pack(pady=20)
btn2 = Button(root, text='选择需要转换excel文件', command=lambda:changeFile(2))
btn2.pack(pady=10)



root.mainloop()
