import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('百度')  #窗口标题
        self.setGeometry(50,30,1355,730)  #窗口的大小和位置设置
        self.browser=QWebEngineView()
        #加载外部的web界面
        self.browser.load(QUrl('file:///D:/5-Python/PythonCode/pyqt5/add_map/test.html'))
        self.setCentralWidget(self.browser)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=MainWindow()
    win.show()
    app.exit(app.exec_())
