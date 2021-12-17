# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtWebEngineWidgets import *
# import sys
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(QMainWindow, self).__init__()
#         self.setWindowTitle('显示网页')
#         self.resize(800, 800)
#         # 新建一个QWebEngineView()对象
#         self.qwebengine = QWebEngineView(self)
#         # 设置网页在窗口中显示的位置和大小
#         self.qwebengine.setGeometry(20, 20, 600, 600)
#         # 在QWebEngineView中加载网址
#         self.qwebengine.load(QUrl(r"file:///D:/5-Python/PythonCode/pyqt5/add_map/test.html"))
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = MainWindow()
#     win.show()
#     sys.exit(app.exec_())


import folium
bj_map = folium.Map(location=[39.93, 116.40], zoom_start=12, tiles='Stamen Toner')

folium.Circle(
    radius=200,
    location=[39.92, 116.43],
    # popup='The Waterfront',
    color='crimson',
    fill=True,
).add_to(bj_map)

# folium.CircleMarker(
#     location=[39.93, 116.38],
#     radius=50,
#     popup='Laurelhurst Park',
#     color='#3186cc',
#     fill=True,
#     fill_color='#3186cc'
# ).add_to(bj_map)

bj_map.save('bj_map.html')