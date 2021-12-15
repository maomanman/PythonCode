# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(496, 261)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 40, 72, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 72, 16))
        self.label_2.setObjectName("label_2")
        self.user_textBrower = QtWidgets.QTextEdit(Form)
        self.user_textBrower.setGeometry(QtCore.QRect(250, 20, 181, 81))
        self.user_textBrower.setObjectName("user_textBrower")
        self.user_lineEdit = QtWidgets.QLineEdit(Form)
        self.user_lineEdit.setGeometry(QtCore.QRect(100, 40, 113, 22))
        self.user_lineEdit.setObjectName("user_lineEdit")
        self.pwd_lineEdit = QtWidgets.QLineEdit(Form)
        self.pwd_lineEdit.setGeometry(QtCore.QRect(100, 70, 113, 22))
        self.pwd_lineEdit.setObjectName("pwd_lineEdit")
        self.login_Button = QtWidgets.QPushButton(Form)
        self.login_Button.setGeometry(QtCore.QRect(60, 150, 97, 29))
        self.login_Button.setObjectName("login_Button")
        self.cancle_Button = QtWidgets.QPushButton(Form)
        self.cancle_Button.setGeometry(QtCore.QRect(270, 140, 97, 29))
        self.cancle_Button.setObjectName("cancle_Button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "用户名"))
        self.label_2.setText(_translate("Form", "密码"))
        self.login_Button.setText(_translate("Form", "登录"))
        self.cancle_Button.setText(_translate("Form", "取消"))

