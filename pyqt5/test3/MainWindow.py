# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test3.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(972, 558)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.clear_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_button.setGeometry(QtCore.QRect(610, 460, 93, 28))
        self.clear_button.setObjectName("clear_button")
        self.load_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_button.setGeometry(QtCore.QRect(750, 460, 93, 28))
        self.load_button.setObjectName("load_button")
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(570, 80, 351, 271))
        self.image_label.setObjectName("image_label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(630, 380, 75, 16))
        self.label_2.setObjectName("label_2")
        self.fileID_button = QtWidgets.QPushButton(self.centralwidget)
        self.fileID_button.setGeometry(QtCore.QRect(720, 370, 93, 28))
        self.fileID_button.setObjectName("fileID_button")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setEnabled(True)
        self.table.setGeometry(QtCore.QRect(20, 20, 531, 481))
        self.table.setMouseTracking(True)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 972, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.clear_button.setText(_translate("MainWindow", "clear"))
        self.load_button.setText(_translate("MainWindow", "load"))
        self.image_label.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "文件序号："))
        self.fileID_button.setText(_translate("MainWindow", "1"))

