# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
#导入程序运行必须模块
import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.Qt import QWidget, QApplication,QTableWidgetItem
#导入designer工具生成的login模块
from test3 import Ui_MainWindow

import psycopg2

class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.clear_button.clicked.connect(self.clear)
        self.load_button.clicked.connect(self.load)
        self.show()


    def clear(self):
        pass


    def load(self):
        conn = psycopg2.connect("dbname=test1_data user=jm password=123")
        cur = conn.cursor()
        cur.execute('select * from table1')
        rows = cur.fetchall()
        row = cur.rowcount  # 取得记录个数，用于设置表格的行数
        vol = len(rows[0])  # 取得字段数，用于设置表格的列数
        cur.close()
        conn.close()

        self.table.setRowCount(row)
        self.table.setColumnCount(vol)

        for i in range(row):
            for j in range(vol):
                temp_data = rows[i][j]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.table.setItem(i, j, data)
if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())