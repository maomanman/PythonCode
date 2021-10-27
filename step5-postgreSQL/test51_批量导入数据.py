import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement
import numpy as np
import os
import re
import json


# 数据写入函数：
def write_gis(path):
    map_data = gpd.GeoDataFrame.from_file(path)
    map_data['geometry'] = map_data['geometry'].apply(lambda x: WKTElement(x.wkt, 4326))
    map_data.drop(['center', 'parent'], axis=1, inplace=True)
    map_data.to_sql(
        name=re.split('\\.', path)[0],
        con=engine,
        if_exists='replace',
        dtype={'geometry': Geometry(geometry_type='POLYGON', srid=4326)}
    )
    return None


# 创建批量任务
def to_do(file_path, username, password, dbname):
    os.chdir(file_path)
    link = "postgresql://{0}:{1}@localhost:5432/{2}".format(username, password, dbname)
    engine = create_engine(link, encoding='utf-8')
    file_list = os.listdir()
    map(lambda x: write_gis(x), file_list)
    return None


# 执行任务计划
if __name__ == '__main__':
    file_path = 'D:/R/mapdata/Province'
    username = 'postgres'
    password = ** ** *
    dbname = 'mytest'
    to_do(file_path, username, password, dbname)
    print('DODE')