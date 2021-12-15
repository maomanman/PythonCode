# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test1.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.test1_button = QtWidgets.QPushButton(Form)
        self.test1_button.setGeometry(QtCore.QRect(80, 190, 93, 28))
        self.test1_button.setObjectName("test1_button")
        self.test1_lineEdit = QtWidgets.QLineEdit(Form)
        self.test1_lineEdit.setGeometry(QtCore.QRect(40, 70, 113, 21))
        self.test1_lineEdit.setObjectName("test1_lineEdit")
        self.test1_Browser = QtWidgets.QTextBrowser(Form)
        self.test1_Browser.setGeometry(QtCore.QRect(180, 40, 191, 81))
        self.test1_Browser.setObjectName("test1_Browser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.test1_button.setText(_translate("Form", "PushButton"))

