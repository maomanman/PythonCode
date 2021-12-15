import pandas as pda
import matplotlib.pyplot as plt

def plotLine():
    data = pda.read_excel(r'D:\mmm\实验数据\test25-小论文实验数据准备\test25-作业效率汇总.xlsx')

    data.sort_values(by = '作业面积平方米',inplace=True)
    # data = data[data.作业面积平方米 < 1500]
    # data = data[data.作业面积平方米 >= 1500]
    # data = data[data.作业面积平方米 < 3600]
    # data =data[data.作业面积平方米 >= 3600]
    data =data[data.作业面积平方米 < 200000]

    plt.rcParams['font.sans-serif'] = ['SimHei']

    data_mean = data.groupby('面积组100')['作业效率（m2/s）'].mean()

    data_big = data[data.作业面积平方米 >= 3600].copy()
    data_mid = data[data.作业面积平方米 < 3600].copy()
    data_mid = data_mid[data_mid.作业面积平方米 >= 1500]
    data_sma = data[data.作业面积平方米 < 1500].copy()

    sma_mean = data_sma.groupby('面积组100')['作业效率（m2/s）'].mean()
    mid_mean = data_mid.groupby('面积组100')['作业效率（m2/s）'].mean()
    big_mean = data_big.groupby('面积组1000')['作业效率（m2/s）'].mean()


    data_r = data[data.作业模式 =='绕行法'].copy()
    data_r.sort_values(by = '作业面积平方米',inplace=True)

    data_t = data[data.作业模式 =='套行法'].copy()
    data_t.sort_values(by = '作业面积平方米',inplace=True)

    data_s = data[data.作业模式 =='梭行法'].copy()
    data_s.sort_values(by = '作业面积平方米',inplace=True)

    data_x = data[data.作业模式 =='斜行法'].copy()
    data_x.sort_values(by = '作业面积平方米',inplace=True)

    r_mean = data_r.groupby('面积组')['作业效率（m2/s）'].mean()
    t_mean = data_t.groupby('面积组')['作业效率（m2/s）'].mean()
    s_mean = data_s.groupby('面积组')['作业效率（m2/s）'].mean()
    x_mean = data_x.groupby('面积组')['作业效率（m2/s）'].mean()

    # x_r=data_r.loc[:,'作业面积平方米']
    # y_r=data_r.loc[:,'作业效率（m2/s）']
    #
    # x_t=data_t.loc[:,'作业面积平方米']
    # y_t=data_t.loc[:,'作业效率（m2/s）']
    #
    # x_s=data_s.loc[:,'作业面积平方米']
    # y_s=data_s.loc[:,'作业效率（m2/s）']
    #
    # x_x=data_x.loc[:,'作业面积平方米']
    # y_x=data_x.loc[:,'作业效率（m2/s）']

    small_mean = data[data.面积组100 < 1500]['作业效率（m2/s）'].mean()
    t = data[data.面积组100 >= 1500]
    midle_mean = t[t.面积组100 < 3600]['作业效率（m2/s）'].mean()
    bigg_mean = data[data.面积组100 >= 3600]['作业效率（m2/s）'].mean()

    plt.grid('both')


    plt.plot([1500]*2,[0,15],'r',[3600]*2,[0,15],'r')
    plt.plot([0,200000],[small_mean]*2,'--b',[1500,200000],[midle_mean]*2,'--g',[3600,200000],[bigg_mean]*2,'--c',)
    plt.plot(sma_mean,'<-b',mid_mean,'^-g',big_mean,'*-c')
    # plt.plot(r_mean,'*-r',t_mean,'^-g',s_mean,'<-b',x_mean,'>-y')
    # plt.plot(x_r,y_r,'*-r',x_t,y_t,'^-g',x_s,y_s,'<-b',x_x,y_x,'>-y')
    # plt.legend(['绕行','套行','梭行','斜行'])
    # plt.plot(x_r,y_r,'*-r')
    # plt.legend({'绕行'})
    plt.title('梭行')
    # plt.subplot(221)
    # plt.plot(data_r.loc[:,'作业面积平方米'],data_r.loc[:,'作业效率（m2/s）'])
    # plt.subplot(222)
    # plt.plot(data_t.loc[:,'作业面积平方米'],data_t.loc[:,'作业效率（m2/s）'])
    # plt.subplot(223)
    # plt.plot(data_s.loc[:,'作业面积平方米'],data_s.loc[:,'作业效率（m2/s）'])
    # plt.subplot(224)
    # plt.plot(data_x.loc[:,'作业面积平方米'],data_x.loc[:,'作业效率（m2/s）'])
    # data_r.plot(x='作业面积平方米',y='作业效率（m2/s）')
    # plt.savefig('D:\mmm\参考文献\我的小论文\小论文插图\效率分析-中等面积.svg',float='svg')
    plt.show()



def plotAreasFactor():
    """
    绘制面积影响因素的折线图
    :return:
    """

    data = pda.read_excel(r'D:\mmm\实验数据\test25-小论文实验数据准备\test25-作业效率汇总.xlsx')

    data.sort_values(by='作业面积平方米', inplace=True)

    data = data[data.作业面积平方米 < 200000]
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # 按  ”面积100“进行分组，组长100，
    data_mean = data.groupby('面积组100')['作业效率（m2/s）'].mean()


    # 将 数据 按面积进行分类，小（< 1500）-中（>= 1500 < 3600）-大（>= 3600）
    data_sma = data[data.作业面积平方米 < 1500].copy()
    data_mid = data[data.作业面积平方米 < 3600].copy()
    data_mid = data_mid[data_mid.作业面积平方米 >= 1500]
    data_big = data[data.作业面积平方米 >= 4000].copy()

    # 对每类（小中大） 的 作业效率 求 均值
    sma_mean = data_sma.groupby('面积组100')['作业效率（m2/s）'].mean()
    mid_mean = data_mid.groupby('面积组100')['作业效率（m2/s）'].mean()
    big_mean = data_big.groupby('面积组1000')['作业效率（m2/s）'].mean()


    #将所有数据分组，并用该组的均值代替该组的效率
    small_mean = data[data.面积组100 < 1500]['作业效率（m2/s）'].mean()
    t = data[data.面积组100 >= 1500]
    midle_mean = t[t.面积组100 < 3600]['作业效率（m2/s）'].mean()
    bigg_mean = data[data.面积组100 >= 3600]['作业效率（m2/s）'].mean()

#figsize=(20, 15), dpi=100
    fig = plt.figure(figsize=(20, 15), dpi=115)
    # plt.grid('both')

    # 添加一个子图
    axe1 = fig.add_axes([0.1,0.1,0.8,0.8])
    # 绘制 地块大小分界线 x= 1500,x=3600
    axe1.plot([1500] * 2, [0, 15], 'r', [3600] * 2, [0, 15], 'r')
    axe1.text(1500,7.5,'X=1500',ha='right',rotation=90,fontdict={'size':'12','color':'r'})
    axe1.text(3600, 7.5, 'X=3600', ha='left', rotation=90, fontdict={'size': '12', 'color': 'r'})
    # 绘制 大中小 地块的平均作业效率
    axe1.plot([0, 200000], [small_mean] * 2, '--b', [1500, 200000], [midle_mean] * 2, '--g', [3600, 200000],[bigg_mean] * 2, '--c')
    axe1.text(100000,small_mean, '小块面积作业效率均值：y='+str(round(small_mean,2)), ha='left', fontdict={'size': '12', 'color': 'b'})
    axe1.text(100000,midle_mean,  '中等面积作业效率均值：y='+str(round(midle_mean,2)), ha='left', fontdict={'size': '12', 'color': 'g'})
    axe1.text(100000, bigg_mean, '大块面积作业效率均值：y='+str(round(bigg_mean,2)), ha='left', fontdict={'size': '12', 'color': 'c'})
    # 绘制 按面积分组后的 作业效率点
    line = axe1.plot(sma_mean, 's-b', mid_mean, '^-g', big_mean, '*-c')
    axe1.legend(line,['小块面积', '中等面积', '大块面积'],loc="upper right")
    axe1.grid('both')
    axe1.set_title('面积大小对作业效率影响',fontdict={'size': '12'})
    axe1.set_xlabel('面积（m2）',fontdict={'size': '12'})
    axe1.set_ylabel('作业效率（m2/s）',fontdict={'size': '12'})

    # axe1.bar()

    # 添加一个子图
    # 这个子图是将 小中地块的作业效率点进行放大显示
    axe2 = fig.add_axes([0.58, 0.62, 0.25, 0.25])
    # 绘制 地块大小分界线 x= 1500,x=3600
    axe2.plot([1500] * 2, [0, 2], 'r', [3600] * 2, [0, 2], 'r')
    axe2.text(1500, 0, 'X=1500', ha='left',  fontdict={'size': '10', 'color': 'r'})
    axe2.text(3600, 0, 'X=3600', ha='left',  fontdict={'size': '10', 'color': 'r'})
    # 绘制 大中小 地块的平均作业效率
    axe2.plot([0, 4000], [small_mean] * 2, '--b', [1500, 4000], [midle_mean] * 2, '--g' )
    axe2.text(3600, small_mean, 'y=' + str(round(small_mean, 2)), ha='left', fontdict={'size': '12', 'color': 'b'})
    axe2.text(3600, midle_mean, 'y=' + str(round(midle_mean, 2)), ha='left', fontdict={'size': '12', 'color': 'g'})
    # 绘制 按面积分组后的 作业效率点
    axe2.plot(sma_mean, 's-b', mid_mean, '^-g')
    axe2.grid('both')

    # 保存为 矢量图
    plt.savefig('D:\mmm\参考文献\我的小论文\小论文插图\面积对作用效率的影响-可视化.svg',float='svg')
    plt.show()


def plotModeFactor():
    """
    绘制 作业模式对作业效率的影响
    :return:
    """

    data = pda.read_excel(r'D:\mmm\实验数据\test25-小论文实验数据准备\test25-作业效率汇总.xlsx')

    # data.sort_values(by='作业效率（m2/s）', inplace=True)
    # data = data[data.作业面积平方米 < 1500]
    # data = data[data.作业面积平方米 >= 1500]
    # data = data[data.作业面积平方米 < 3600]
    data =data[data.作业面积平方米 >= 3600]
    data = data[data.作业面积平方米 >= 40000]

    plt.rcParams['font.sans-serif'] = ['SimHei']


    data_r = data[data.作业模式 == '绕行法']
    data_t = data[data.作业模式 == '套行法']
    data_s = data[data.作业模式 == '梭行法']
    data_x = data[data.作业模式 == '斜行法']

    r_mean = data_r.groupby('面积组')['作业效率（m2/s）'].mean()
    t_mean = data_t.groupby('面积组')['作业效率（m2/s）'].mean()
    s_mean = data_s.groupby('面积组')['作业效率（m2/s）'].mean()
    x_mean = data_x.groupby('面积组')['作业效率（m2/s）'].mean()



    plt.grid('both')


    plt.plot(r_mean,'*-r',t_mean,'^-g',s_mean,'s-b',x_mean,'>-y')
    # plt.plot(x_r,y_r,'*-r',x_t,y_t,'^-g',x_s,y_s,'<-b',x_x,y_x,'>-y')
    plt.legend(['绕行','套行','梭行','斜行'])
    # plt.plot(x_r,y_r,'*-r')
    # plt.legend({'绕行'})
    plt.title('40000 <= 面积 ',fontdict={'size': '12'})
    # plt.subplot(221)
    # plt.plot(data_r.loc[:,'作业面积平方米'],data_r.loc[:,'作业效率（m2/s）'])
    # plt.subplot(222)
    # plt.plot(data_t.loc[:,'作业面积平方米'],data_t.loc[:,'作业效率（m2/s）'])
    # plt.subplot(223)
    # plt.plot(data_s.loc[:,'作业面积平方米'],data_s.loc[:,'作业效率（m2/s）'])
    # plt.subplot(224)
    # plt.plot(data_x.loc[:,'作业面积平方米'],data_x.loc[:,'作业效率（m2/s）'])
    # data_r.plot(x='作业面积平方米',y='作业效率（m2/s）')
    plt.savefig('D:\mmm\参考文献\我的小论文\小论文插图\效率分析-大块面积2.svg',float='svg')
    plt.show()


# 绘制 面积影响的 效率图
plotAreasFactor()
#绘制 作业模式对作业效率的影响
# plotModeFactor()