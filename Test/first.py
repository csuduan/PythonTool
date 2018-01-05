import pymysql
import pymssql
import numpy as np
import pandas as pd
import time


#pd.set_option('display.height',1000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)


account='阳月一号'
startDate='20170714'

#获取收益数据
date=time.strftime("%Y%m%d",time.localtime(time.time()))

sqlReal=f''' select * from tools.profit where account='{account}' and profitType='REAL' and settledate>='{startDate}'  
         '''
sqlAccountConfig=f''' select * from AccountConfig where 名称='{account}' 
                  '''
sqlStrategyProfitRate=f''' SELECT  * from StrategySummaryView a left join StrategyInfo b on a.StrategyID=b.StrategyID 
                            where b.Owner='段晴' and TradingDay>='{startDate}'
                       '''

conn = pymysql.connect("192.168.1.38","guest","guest","tools",charset='utf8')
dfReal = pd.read_sql(sqlReal, conn)
conn.close()

conn1=pymssql.connect('192.168.1.10','duanqing','duanqing','strategy',charset='utf8')
dfAccountConfig=pd.read_sql(sqlAccountConfig,conn1)
dfStrategyProfitRate=pd.read_sql(sqlStrategyProfitRate,conn1)

conn1.close()

def calMaketValue(item):
    marketValue=0
    if item['StrategyType']=='StrategyTrend2':
        marketValue=item['TREND2比例']*item['规模']
    else:
        marketValue=item['TREND1比例']*item['规模']

    item['marketValue']=marketValue
    return  item


df2=dfStrategyProfitRate.merge(dfAccountConfig,right_on='TradingDay',left_on='TradingDay',how = 'left')
df2['marketValue']=-1

df3=df2.apply(calMaketValue,axis=1)

# for index,item in df2.iterrows():
#     marketValue=0
#     if item['StrategyType']=='StrategyTrend2':
#         marketValue=item['TREND2比例']*item['规模']
#     else:
#         marketValue=item['TREND1比例']*item['规模']
#
#     item['marketValue']=marketValue

df3['profit']=df3['NetChange']*df3['marketValue']*10000
df4=df3.groupby(['TradingDay'])['profit'].sum()
pass