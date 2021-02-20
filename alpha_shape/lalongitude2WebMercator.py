import pandas as pda
import numpy as npy
# import math as ma
import datetime
# 这两个是用于的打开文件选择框
from tkinter import Tk
from tkinter.filedialog import askopenfilename

window = Tk()
window.withdraw()
file_name = askopenfilename(title='打开文件', filetypes=[('All File', '*')])

# window.mainloop()
del window

data = pda.read_excel(file_name)

earthRad = 6378137.0

lng = npy.array(data['经度'])
lat = npy.array(data['纬度'])

x = lng * npy.pi / 180 * earthRad
a = lat * npy.pi / 180
y = earthRad / 2 * npy.log((1.0 + npy.sin(a)) / (1.0 - npy.sin(a)))

# x = lng * 20037508.34 / 180
# y = npy.log(npy.tan((90 + lat) * npy.pi / 360)) / (npy.pi / 180)
# y = y *20037508.34/180

# data['x'] = x
# data['y'] = y

# 60002
# data['x']=x+268.7547253
# data['y']=y+142.8472509

# 19023
# data['x']=x+268.7547253 +105.38
# data['y']=y+142.8472509 -24.193

# y3616
# data['x']=x+268.7547253 +24.431
# data['y']=y+142.8472509 -148.875

# 98765
data['x'] = x + 323.4876526


data['y'] = y + 174.7519493



data.set_index('序列号', inplace=True)

timeStamp = datetime.datetime.now().strftime('%m%d-%H%M%S')
f = file_name.split('.')
path_name_exl = f[0] + '-2墨卡托坐标' + timeStamp + '.' + f[1]
data.to_excel(path_name_exl)
path_name_csv = f[0] + '-2墨卡托坐标' + timeStamp + '.csv'
data.to_csv(path_name_csv)
