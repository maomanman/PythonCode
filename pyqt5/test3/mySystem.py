# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
#导入程序运行必须模块
import sys
import os
import glob #用于模糊匹配获得文件名
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.Qt import QWidget, QApplication,QTableWidgetItem
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QUrl,QRect ,pyqtSignal

#导入designer工具生成的login模块
from MainWindow import Ui_MainWindow
from ChildWindow import Ui_ChildDialog as U2

import psycopg2 # 用于链接postgre数据库
from PyQt5.QtWebEngineWidgets import * # 用于加载网页

from LoadOnLineMap import PlotLineOnMap  #加载卫星地图+轨迹展示
from globalVal import globalVal # 全局变量
from connPostSQL import PostSql




#主窗口
class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        if globalVal.debug :
            print("创建主窗口")

        # 定义信号，用于跟子窗口传递数据 含一个int型参数的信号
        self.signal_fileID = pyqtSignal(int)

        # 初始化表格显示数据
        MyMainForm.load(self)
        self.clear_button.clicked.connect(self.clear) # 按钮清空表格
        self.load_button.clicked.connect(self.load) # 按钮装载数据
        # self.show()

        # 用label 显示图片--用于根据鼠标选中单元格所对应的轨迹图  初始化显示1号文件图
        pix = QPixmap(r'D:\mmm\轨迹数据集\轨迹图汇总\edgeImage\00001_edgeImage_R=8.58.jpg')
        self.image_label.setPixmap(pix)
        self.image_label.setScaledContents(True)  # 缩放图片以填充label空间

        # 用鼠标点击表格 选择文件显示其轨迹图片
        self.table.clicked.connect(self.getItem) #链接槽函数

        # 创建子窗口对象 ，暂时先不展示，触发事件后展示
        self.win2 = MyChildForm()

        # 显示文件序号的按钮 的 单击事件 绑定 槽函数--弹出子窗口
        self.fileID_button.clicked.connect(self.showChildWindow)

        # 导入轨迹文件
        self.inputFile_button.clicked.connect(self.inputFile)

    #点击文件序号按钮 弹出子窗口
    def showChildWindow(self):

        # 根据文件序号 ，将轨迹点绘制在 遥感天地图上---加载的卫星地图用html文件保存，以备后续在窗口显示
        PlotLineOnMap(self.fileID_button.text())


        if globalVal.debug:
            print("刷新子界面的网页",globalVal.mapPath)
        self.win2.browser.load(QUrl(globalVal.mapPath))

        # 显示子窗口
        self.win2.show()
        if globalVal.debug:
            print("显示子窗口")


    #清楚表格数据
    def clear(self):
        #清除表格数据
        self.table.clear()

        # 恢复默认展示1号文件轨迹图
        imageName= glob.glob(os.path.join(globalVal.imageBasePath, str(1).zfill(5)) + '_edgeImage_R*')
        pix = QPixmap(imageName[0])
        self.image_label.setPixmap(pix)
        self.image_label.setScaledContents(True)  # 缩放图片以填充label空间
        self.fileID_button.setText(str(1).zfill(5))  # 显示当前图片的文件序号

    # 鼠标移动 获取表格数据
    def getItem(self):
        # 获取单元格的值
        row = self.table.selectedItems()[0].row()
        fileID = self.table.item(row,3).text() # 根据行列号获取单元格数据，行列号都是从0开始计算

        self.showImage(fileID)

        #发射信号，将文件序号传递给子窗口
        # self.signal_fileID.emit(fileID)
        self.win2.fileID = fileID
        # 根据文件序号 ，将轨迹点绘制在 遥感天地图上---加载的卫星地图用html文件保存，以备后续在窗口显示
        PlotLineOnMap(self.fileID_button.text())
        self.win2.browser.load(QUrl(globalVal.mapPath))
        self.win2.showValues(fileID)

    # 根据文件号 展示对应的轨迹图
    def showImage(self,fileID):

        #根据文件序号，用模糊匹配查找图片名称，注意返回的 imageName 是 列表，
        imageName = glob.glob(os.path.join(globalVal.imageBasePath,str(fileID).zfill(5))+'_edgeImage_R*')

        # 用label 显示图片
        pix = QPixmap(imageName[0]) # imageName 是列表属性
        self.image_label.setPixmap(pix)
        self.image_label.setScaledContents(True)  # 缩放图片以填充label空间
        self.fileID_button.setText(str(fileID).zfill(5)) # 显示当前图片的文件序号

    # 从数据库下载数据
    def load(self):
        # conn = psycopg2.connect("dbname=postsql_test user=postgres password=123456")
        # cur = conn.cursor()
        # cur.execute('select * from tb_field_info ')
        # rows = cur.fetchall()
        # row = cur.rowcount  # 取得记录个数，用于设置表格的行数
        # vol = len(rows[0])  # 取得字段数，用于设置表格的列数
        # cur.close()
        # conn.close()

        rows = mydb.cursor('select * from tb_field_info ')
        row = len(rows)# 取得记录个数，用于设置表格的行数
        vol = len(rows[0])  # 取得字段数，用于设置表格的列数

        self.table.setRowCount(row)
        self.table.setColumnCount(vol)

        for i in range(row):
            for j in range(vol):
                temp_data = rows[i][j]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.table.setItem(i, j, data)

    # 导入轨迹文件
    def inputFile(self):
        fp = QFileDialog.getOpenFileName(None,"选择文件","D:/mmm/轨迹数据集/汇总/","All Files(*)")
        self.filePath_lineEdit.setText(fp[0]) # 显示选择的文件

# 子窗口
class MyChildForm(QMainWindow, U2):
    def __init__(self, parent=None):
        super(MyChildForm, self).__init__(parent)
        self.setupUi(self)
        self.fileID = 1 # 初始化的文件序号为1
        # mapPath = self.PlotLineOnMap()
        self.setWindowTitle("子窗口")

        #设置显示地图的窗口
        self.browser = QWebEngineView(self)
        self.browser.setGeometry(20, 20, 411, 491)


        if globalVal.debug:
            print("创建子窗口")

        #显示边界图
        self.edgeMap_button.clicked.connect(self.edgeMapButtonClicked)

        #显示路径图
        self.traMap_button.clicked.connect(self.traMapButtonClicked)

        # 显示工作轨迹点
        self.workMap_button.clicked.connect(self.workMapButtonClicked)

        #显示相关效率值
        self.showValues(self.fileID)

    def edgeMapButtonClicked(self):
        """
        显示 卫星底图 + 作业地块边界线
        :return:
        """
        PlotLineOnMap(self.fileID,fileType = 2)
        if globalVal.debug:
            print(globalVal.edgeMapPath)
        self.browser.load(QUrl(globalVal.edgeMapPath))

    def traMapButtonClicked(self):
        """
        显示轨迹图
        :return:
        """
        self.browser.load(QUrl(globalVal.mapPath))

    def workMapButtonClicked(self):
        """
        将工作轨迹点个非工作轨迹点区别显示
        :return:
        """
        PlotLineOnMap(self.fileID, fileType=3)
        if globalVal.debug:
            print("显示工作点",globalVal.workMapPath)
        self.browser.load(QUrl(globalVal.workMapPath))
        pass

    # def getFileID(self,fileID):
    #     """
    #     # 定义传递文件序号的信号的槽函数
    #     :param fileID: 参数是由信号发射时传递
    #     :return:
    #     """
    #     if globalVal.debug:
    #         print("从主窗口传过来的文件序号",fileID)
    #     self.fileID=fileID
    #     pass

    def showValues(self,fileID):
        """
        根据文件号显示轨迹的相关效率值
        :return:
        """
        info = mydb.cursor('select * from tb_field_ratio where "fileID"='+str(fileID))
        self.totalTime_lineEdit.setText(str(info[0][1]))
        self.workTime_lineEdit.setText(str(info[0][2]))

        self.totalDistance_lineEdit.setText(str(info[0][3]))
        self.workDistance_lineEdit.setText(str(info[0][4]))

        self.area_lineEdit.setText(str(info[0][5]))
        self.timeRatio_lineEdit.setText(str(info[0][2]/info[0][1]))
        self.distanceRatio_lineEdit.setText(str(info[0][4]/info[0][3]))
        self.ratio_lineEdit.setText(str(info[0][5]/info[0][1]))


if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)

    #链接数据库
    mydb = PostSql()

    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()

    app.exec_()
    # 断开数据库链接
    mydb.disconnectSQL()
    # print('关闭数据库')
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit()

