import pandas as pda
import numpy as np
import matplotlib.pyplot as plt

def plotArea():
    """
    根据面积大小 绘制 直方图
    :return:
    """
    data = pda.read_excel(r'D:\mmm\实验数据\test15-坐标转换纠正\test15_轨迹索引_v2.0.xlsx')
    data.set_index('新文件序号',inplace=True,drop=True)
    # data = data[~(data['边界视察']>0)]
    diqu=['新疆','黑龙江省','山东省','安徽','辽宁','湖南']
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    num = 0
    for s in diqu:
        sheng = data[data['省']==s]


        # wide_bin_df = pda.cut(sheng['作业面积亩'],bins=[0, 11, 21, 31, 41, 51, 61, 71, 81,91,101,201,2000],
        #                      right=False, labels=['小于10','11-20', '21-30', '31-40','41-50', '51-60', '61-70','71-80','81-90','91-100','101-200', '201以上'])
        wide_bin_df = pda.cut(sheng['作业面积亩'], bins=[0,2, 11, 2000],
                              right=False,
                              labels=['小于2亩','2-10亩', '11亩以上'])

        # print('wide_count:')
    # print(pda.value_counts(wide_bin_df))

        axdata = pda.value_counts(wide_bin_df).sort_index()

    # ax = axdata.plot(kind='bar',rot=45,title='山东省')
        ind = np.arange(0,len(axdata))*3
        plt.bar(ind+ num * 0.3,axdata[:],0.3)

        for i ,a in zip(ind+num * 0.3,axdata.index):
            # print(a)
            b=axdata[a]
            if b!=0:
                plt.text(i, b, '%.0f' % b, ha='center', va= 'bottom',fontsize=11)
        num = num + 1

    plt.xticks(ind + (num-1)*0.15, axdata.index)
    # plt.xticks(rotation=60)
    plt.legend(diqu)
    plt.title('各地块面积大小情况分布')
    plt.show()

plotArea()