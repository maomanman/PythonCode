import os
import pandas as pd
import tkinter.messagebox
from tkinter.filedialog import *

import re

def changeImage():
    pass

root = Tk()
root.title('excel2cvs')
root.geometry("400x200")
# label1 = Label(root, text='原文件类型', height=1, width=20, fg="black")
# label1.pack(pady=10)
label2 = Label(root, text='', height=1, width=20, fg="black")
label2.pack()
btn1 = Button(root, text='选择需要转换成csv文件', command=changeImage)
btn1.pack(pady=20)
btn2 = Button(root, text='选择需要转换excel文件', command=lambda: changeFile(2))
btn2.pack(pady=10)

root.mainloop()