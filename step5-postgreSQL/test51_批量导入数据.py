import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement
import numpy as np
import os
import re
import json
import psycopg2
import time

# 数据写入函数：
def write_gis(data,engine,path=None):
    # gs = gpd.GeoSeries.from_wkt(data['wkt'])
    # map_data = gpd.GeoDataFrame.from_file(path,encoding='utf-8')
    map_data = gpd.GeoDataFrame(data)
    # map_data['geometry'] = map_data['geometry'].apply(map_data['geometry'])
    # map_data['geometry'] = map_data['x'].apply(WKTElement(map_data['x']))
    # map_data.drop(['wkt'], axis=1, inplace=True)

    # count = map_data.shape[0]
    #
    # for i in range(count):
    #     map_data.loc[i,'geometry'] = WKTElement(map_data.loc[i,'x'] )
    map_data.rename(columns={"fileIndex":"file_index", "速度(km/h)":"速度","幅宽(m)":"幅宽", "深度(mm)":"深度",'geometry':'geom'},inplace=True)
    map_data.set_index('序列号',inplace=True)
    map_data.to_sql(
        name=re.split('\\.', path)[0],
        con=engine,
        if_exists='append',
        dtype={'geometry': Geometry(geometry_type='POINT')}
    )
    return None


# 创建批量任务
def to_do(file_path, username, password, dbname):
    # global  engine
    os.chdir(file_path)
    link = "postgresql://{0}:{1}@localhost:5432/{2}".format(username, password, dbname)
    engine = create_engine(link, encoding='utf-8')
    file_list = os.listdir()
    data = pd.read_csv(file_path+'/tb_point_info.csv')
    write_gis(data,engine,'tb_point_info.csv')
    #map(lambda x: write_gis(x), file_list)
    return None



###### 自己组装 insert 语句
def test51_import2():
    print("Connecting..") # postgresql://{0}:{1}@localhost:5432/{2}
    # conn_to = psycopg2.connect("host='localhost' port='5432' database=postsql_test user='postsql_test' password='12345'")
    # conn_to = psycopg2.connect("dbname=postsql_test user=postsql_test password=12345")
    # conn_to = psycopg2.connect(host='localhost', port='5432', database='postsql_test', user='postsql_test', password='12345')

    # 链接数据库
    conn_to = psycopg2.connect(
        database='postsql_test',
        user='postgres',
        password='123456',
        host='localhost',
        port='5432')

    # conn_to = psycopg2.connect(host='localhost', port='5432', database='b', user='postgres', password='1234')
    print("Connected.\n")

    # cursor_to = conn_from.cursor()
    cursor_to = conn_to.cursor()
    data = pd.read_csv(r'D:\mmm\实验数据\test27-postgresql\tb_point_info.csv')
    count = data.shape[0]
    i = 0

    # 从数据库中读取数据
    # cursor_to.execute("SELECT * FROM tb_point_info " )
    # results = cursor_to.fetchall()
    # print(results)

    # 插入数据库
    for i  in range(count):
        tr = data.loc[i]

        sql = "begin transaction; INSERT INTO tb_point_info(file_index, \"序列号\", \"GPS时间\", \"经度\", \"纬度\", \"速度\", \"航向\", \"工作状态\", \"幅宽\",\"深度\", geom)" \
              " VALUES(" + str(tr[0]) + "," + str(tr[1]) + ",'" + str(tr[2] )+ "'," + str(tr[3]) + "," + str(tr[4]) + "," + str( \
            tr[5]) + "," + str(tr[6]) + ",'" + str(tr[7]) +"'," + str(tr[8]) +"," + str(tr[9])  + ",POINT(" + str(tr[3]) + "," + str( \
            tr[4]) +  ")::geometry)"
        cursor_to.execute(sql)
        conn_to.commit()
        # i += 1
    # cursor_from.close()
    cursor_to.close()
    # conn_from.close()
    conn_to.close()

def oneImport():
    print("Starting...")
    startTime = time.time()
    test51_import2()
    endTime = time.time()
    print("Completed.")

    print("共耗时" + str(endTime - startTime) + "秒")


# 直接导入文件，系统批量组装insert语句
def fileImport1():
    file_path = r'D:\mmm\实验数据\test27-postgresql'
    username = 'postgres'
    password = '123456'
    dbname = 'postsql_test'
    to_do(file_path, username, password, dbname)
    print('DODE')


########## 按现有轨迹点文件进行批量导入#####################
def connetSQL(username,password,dbname):
    """
    连接数据库
    :param username:
    :param password:
    :param dbname:
    :return:
    """
    link = "postgresql://{0}:{1}@localhost:5432/{2}".format(username, password, dbname)
    engine = create_engine(link, encoding='utf-8')
    return engine

# 写入数据库
def write_postgres(data,engine,tableName):
    map_data = gpd.GeoDataFrame(data)

    map_data.rename(columns={"fileIndex":"file_index", "速度(km/h)":"速度","幅宽(m)":"幅宽", "深度(mm)":"深度",'geometry':'geom'},inplace=True)
    map_data.set_index('序列号',inplace=True)
    map_data.to_sql(
        name=tableName,
        con=engine,
        if_exists='append',
        dtype={'geometry': Geometry(geometry_type='POINT')}
    )
    return None

def createPoint(fileData):

    return 'point(%s %s)::geometry'%(str(fileData['经度']),str(fileData['纬度']))

def batchImportSql(path=None,username ='postgres' , password='123456', dbname='postsql_test'):
    """
    按现有轨迹点的存在形式 批量 导入postgresql
    :param path:
    :param username:
    :param password:
    :param dbname:
    :return:
    """
    path = r'D:\mmm\实验数据\test27-postgresql'
    startTime = time.time()

    # 链接数据库
    dbEngine = connetSQL(username, password, dbname)

    #待写入的数据表
    tableName = 'tb_point_info'

    indexFile = pd.read_excel(path + '/test27-postgresql-轨迹索引-v3.0.xlsx')
    for i,fileName in zip(indexFile.loc[:,'新文件序号'],indexFile.loc[:,'文件名称']): # 每次循环导入一个文件
        start = time.time()
        fileData = pd.read_excel('D:\mmm\轨迹数据集\汇总'+ '/' + fileName)

        # 数据准备
        fileData.loc[:,'fileIndex'] = fileData.apply(lambda x:i,axis = 1) # 记录文件序号
        fileData.loc[:,'geometry'] = fileData.apply(createPoint,axis = 1) # 创建geometry数据

        # 数据库导入
        write_postgres(fileData, dbEngine, tableName)

        end = time.time()
        print('%d号文件已导入，耗时 %lf 秒' % (i, end - start))
        del fileData

    endTime = time.time()
    print('导入所有文件共耗时' + str(endTime - startTime) + '秒')

# 执行任务计划
if __name__ == '__main__':
    # fileImport1()
    # oneImport()
    batchImportSql()  # 批量导入
