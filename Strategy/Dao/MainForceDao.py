import pandas as pd
import pymysql

class MainForceDao(object):
    @staticmethod
    def QryMainForce(product):
        conn = pymysql.connect("127.0.0.1","csuduan","715300","tools",charset='utf8')
        sql=f'''
            SELECT * FROM tools.mainforcemapping where product='{product}'
        '''
        df=pd.read_sql(sql,conn)
        return  df