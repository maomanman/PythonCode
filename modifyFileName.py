import os
import pandas as pda

bastP = r'D:\mmm\轨迹数据集\test12\equalImage\第一批'
# modifyFN_info=pda.DataFrame(columns=['原文件名','现文件名','目标文件名','flag'])
# data = pda.read_excel(r'D:\mmm\轨迹数据集\轨迹索引-v1.0.xlsx')
# srcFL = os.listdir(r'D:\mmm\轨迹数据集\汇总')
# desFL =data['文件名称'].dropna()
# srcI = 0
#
# for df in desFL:
#     df=df.strip()
#     sf = srcFL[srcI].strip()
#
#     flag = 0
#     if sf != df:
#         if sf.split(' ')[0] == df.split(' ')[0]:
#             os.rename(bastP+ '/'+sf,bastP + '/'+df)
#             flag = 1
#         else:
#             modifyFN_info.loc[srcI] = [sf, df, df, flag]
#             break
#     modifyFN_info.loc[srcI] = [sf,df,df,flag]
#     srcI = srcI + 1
#
#     modifyFN_info.to_excel(r'D:\mmm\轨迹数据集' + '/modifyFN_info.xlsx'   )
#
#
# modifyFN_info.to_excel(r'D:\mmm\轨迹数据集' + '/modifyFN_info.xlsx'   )
# print('over')

sorL = os.listdir(bastP)

for f in sorL:
    des = f.replace('move','equal')
    os.rename(bastP+'/'+f,bastP+'/'+des)