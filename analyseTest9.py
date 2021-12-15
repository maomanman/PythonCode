import pandas as pda
import os
import matplotlib.pyplot as plt


rootPath=r'D:\mmm\轨迹数据集\test9'
fileList = os.listdir(r'D:\mmm\轨迹数据集\test9')

for f in fileList:
    if 'radiusInfo' in f :
        data = pda.read_excel(rootPath+'/'+f)
        # print(data.columns)
        # data.rename(columns={'地块面积（平方米）':'area','Unnamed: 0':'index'},inplace=True)
        # 计算面积变化率
        count = data.shape[0]
        for i in range(0,count-1):
            rate = abs(data.loc[i+1,'area']-data.loc[i,'area'])/data.loc[i,'area']
            if rate >0.05:
                rate = 0.05
            data.loc[i,'面积变化率3']=rate
        data.set_index('index',inplace=True)
        data.to_excel(rootPath+'/'+f)

        # 绘制面积变化率的图
        legendtxt=f.split('_')[0]

        data.rename(columns={'面积变化率3': legendtxt}, inplace=True)
        # if legendtxt =='0':
        #     ax= data.plot.line(x='radius',y=legendtxt,xticks=data.radius,grid='on',figsize =(19.2,9.3))
        # else:
        #     data.plot.line(x='radius', y=legendtxt, xticks=data.radius, grid='on', figsize=(19.2, 9.3),ax=ax)
        data.plot.line(x='radius', y=legendtxt, xticks=data.radius, grid='on', figsize=(19.2, 9.3))
        plt.savefig(rootPath+'/rate3/'+legendtxt+'_rate.png')


        del data

plt.show()
