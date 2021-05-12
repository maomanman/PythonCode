import os
import shutil
import pandas as pda

# bastPath = 'D:/mmm/轨迹数据集/test12/edgePoint'  # 源文件路径名
# desPath =  'D:/mmm/轨迹数据集/test12/edgePoint/errorEdge' # 目标文件路径名
# data = pda.read_excel(r'D:\mmm\轨迹数据集\test12\test12_result_info.xlsx')
#
# srcList = data[data['flag']==0]['edgepointfile'] # 待移动文件名列表
#
# for f in srcList:
#     srcFile = bastPath + '/'+f
#     desFile =desPath + '/' + f
#     shutil.move(srcFile,desFile)


## 登记文件
DIR =  'D:/mmm/轨迹数据集/test12/test12_2/edgePoint'
def compare(x, y):

    stat_x = os.stat(DIR + "/" + x)
    stat_y = os.stat(DIR + "/" + y)
    if stat_x.st_ctime < stat_y.st_ctime:
        return -1
    elif stat_x.st_ctime > stat_y.st_ctime:
        return 1
    else:
        return 0

path =  'D:/mmm/轨迹数据集/test12/test12_2/edgePoint'
fp=r'D:\mmm\轨迹数据集\test12\test12_2\errEdge_info -01.xlsx'

data = pda.read_excel(fp)

edgList = os.listdir(path)
edgList.sort(key=lambda fn: os.path.getmtime(path+'/'+fn))
for i in data.index:
    data.loc[i,'edgepoint'] = edgList[i]

data.to_excel(fp)