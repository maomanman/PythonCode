import psycopg2

class PostSql:
    def __init__(self):
        self.conn = psycopg2.connect("dbname=postsql_test user=postgres password=123456")

    def disconnectSQL(self):
        self.conn.close()

    def cursor(self,str1):

        cur = self.conn.cursor()
        # cur.execute('select * from tb_field_info ')
        cur.execute(str1)
        rows = cur.fetchall()
        # row = cur.rowcount  # 取得记录个数，用于设置表格的行数
        # vol = len(rows[0])  # 取得字段数，用于设置表格的列数
        cur.close()

        return rows

    def insertSQL(self,str1):
        cur = self.conn.cursor()
        ret = cur.execute(str1)
        return ret #插入成功返回1