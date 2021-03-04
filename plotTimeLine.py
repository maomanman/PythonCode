import pandas as pda
import matplotlib.pyplot as plt




def compareTime():
    data = pda.DataFrame(columns=['radius', 'time1', 'time2'])
    for fk in infodata.loc[[0,3,15],'幅宽']:
        name = 'radiusInfo' + str(fk)+'.xlsx'
        data1=pda.read_excel(path1+'/'+name)
        data2=pda.read_excel(path2+'/'+name)


        data.radius=data1.radius
        data.time1=data1.耗时
        data.time2=data2.loc[:,'边界点检测耗时(s)']

        data.plot.bar(x='radius',figsize =(19.2,9.3))
        plt.savefig(path2+'/compareTime-image/'+str(fk).replace('.','_')+'.png')
        plt.savefig(path2 + '/width-' + str(fk).replace('.', '-')+'/' + str(fk).replace('.', '_') + '-times.png')


def compareBestRadius():

    for fk in infodata.loc[:,'幅宽']:
        name = 'radiusInfo' + str(fk)+'.xlsx'
        # data1=pda.read_excel(path1+'/'+name)
        data2=pda.read_excel(path2+'/'+name)

        data2.plot.line(x='radius',y='地块面积（平方米）',xticks=data2.radius,grid='on',figsize =(19.2,9.3))
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
        plt.savefig(path2+'/compareBestRadius-image/'+str(fk).replace('.','_')+'-areas.png')
        plt.savefig(path2 + '/width-' + str(fk).replace('.', '-')+'/' + str(fk).replace('.', '_') + '-areas.png')

        data2.plot.line(x='radius',y='边界点检测耗时(s)',xticks=data2.radius,grid='on',figsize =(19.2,9.3),color='red')
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        # plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
        plt.savefig(path2+'/compareBestRadius-image/'+str(fk).replace('.','_')+'-times.png')
        plt.savefig(path2 + '/width-' + str(fk).replace('.', '-')+'/' + str(fk).replace('.', '_') + '-times.png')

def compareBestRadiusWithSameWidth():

    count = infodata.shape[0]
    for fk in range(1,count-1):
        name = 'radiusInfo_' + str(fk)+'.xlsx'
        # data1=pda.read_excel(path1+'/'+name)
        data2=pda.read_excel(path2+'/'+name)

        data2.plot.line(x='radius',y='地块面积（平方米）',xticks=data2.radius,grid='on',figsize =(19.2,9.3))
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
        plt.savefig(path2+'/compareBestRadius-image/'+str(fk).replace('.','_')+'-areas.png')
        plt.savefig(path2 + '/1-4_num_' + str(fk).replace('.', '-')+'/' + str(fk).replace('.', '_') + '-areas.png')

        data2.plot.line(x='radius',y='边界点检测耗时(s)',xticks=data2.radius,grid='on',figsize =(19.2,9.3),color='red')
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        # plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
        plt.savefig(path2+'/compareBestRadius-image/'+str(fk).replace('.','_')+'-times.png')
        plt.savefig(path2 + '/1-4_num_' + str(fk).replace('.', '-')+'/' + str(fk).replace('.', '_') + '-times.png')

path2 = r'D:\mmm\轨迹数据集\image'
path1 =r'D:\mmm\轨迹数据集\image-20210223'
infoname='widthInfo-1-4.xlsx'
infodata = pda.read_excel(path2+'/'+infoname)

# compareTime()
# compareBestRadius()
compareBestRadiusWithSameWidth()