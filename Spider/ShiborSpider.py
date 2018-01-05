import tushare as ts
import pandas as pd
import pymssql
import sqlalchemy
import time

#SHIBOR爬虫


FullMode=False
engine =sqlalchemy.create_engine('mssql+pymssql://wind:wind@192.168.1.10:1433/wind')
#date=time.strftime('%Y%m%d',time.localtime(time.time()))
date='20170802'
tms=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))



def convertFormat(row):
    date=row[0]
    df1=pd.DataFrame(row.T[1:])
    df1.columns=['B_INFO_RATE']
    df1['OBJECT_ID']=0
    df1['S_INFO_WINDCODE']='SHIBOR'+df1.index+'.IR'
    df1['TRADE_DT']=date
    df1['OPDATE']=tms
    df1['OPMODE']=0
    print(df1)
    if len(df1)>0:
        df1.to_sql('SHIBORPRICES',engine,index=False,if_exists='append')

def main():


    df=ts.shibor_data()
    df['date']=df.date.apply(lambda s:s.strftime('%Y%m%d'))

    engine.connect().execute(f'delete from shiborprices where trade_dt=\'{date}\'')
    df1=df[df['date']==date]
    df1.apply(lambda s:convertFormat(s),axis=1)


if __name__ == '__main__':
    main()