import pandas as pda
import  os
import alpha_shape.AlphaShapeForEdge as selfShape

def test26_calPeri_oneFile(edgeF):
    """
    计算地块的周长：根据边界点
    :return:
    """
    count = edgeF.shape[0]
    peri = 0
    for i in range(count-1):
        peri += selfShape.distance((edgeF.loc[i,'x'],edgeF.loc[i,'y']),(edgeF.loc[i+1,'x'],edgeF.loc[i+1,'y']))

    return peri

def test26_calPeri_total():
    """

    :return:
    """

    fileList = os.listdir('D:\mmm\轨迹数据集\轨迹图汇总\edgePoint')

    resultPeri = pda.DataFrame(columns={'文件序号','周长'})
    i = 0
    for edgeN in fileList:
        edgeF = pda.read_excel(r'D:\mmm\轨迹数据集\轨迹图汇总\edgePoint\\' + edgeN )
        peri = test26_calPeri_oneFile(edgeF)
        print([edgeN[0:5],peri])
        resultPeri.loc[i] = [edgeN[0:5],peri]
        i +=1

    resultPeri.to_excel(r'D:\mmm\实验数据\test26-计算地块周长\test26_resultPeri.xlsx')

#####################################################

# edgeF = pda.read_excel(r'D:\mmm\轨迹数据集\轨迹图汇总\edgePoint\00001_edgePoint_R=8.58.xlsx')
# peri = test26_calPeri_oneFile(edgeF)
#
# print(peri)

test26_calPeri_total()