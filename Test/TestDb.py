import pymssql
import pandas as pd
import pymysql
import pandas as pd
import time

# conn = pymssql.connect(server='192.168.1.10',
#                        port='1433',
#                        user='zhangqian',
#                        password='20161201',
#                        database='WIND',charset='GBK')
#
# sql='''
# SELECT TOP 1000 [WindCode]
#       ,[TradingDay]
#       ,[FirstIndustryName]
#       ,[FirstIndustryCode]
#       ,[OpenPrice]
#       ,[ClosePrice]
#       ,[HighPrice]
#       ,[LowPrice]
#       ,[PrevClosePrice]
#       ,[StockReturn]
#       ,[TurnoverVolume]
#       ,[TurnoverValue]
#       ,[Ashares]
#       ,[NonRestrictedShares]
#       ,[TotalShares]
#       ,[MarketCapA]
#       ,[MarketCapAFloat]
#       ,[MarketCapTotal]
#       ,[MarketReturnHS300]
#       ,[MarketReturnSZ50]
#       ,[MarketReturnZZ500]
#       ,[SplitFactor]
#       ,[RiskFreeRate]
#       ,[IndustryChange]
#       ,[TradeStatus]
#       ,[OPDATE]
#   FROM [DBALPHA].[dbo].[DailyQuote]
# '''
#
# df = pd.read_sql(sql, conn)
#
# print(df)






conn = pymysql.connect("127.0.0.1","csuduan","715300","tools",charset='utf8')
t=time.time()

sql=f'''
  select * from tools.klinedata where date>'20160000' 
'''
df = pd.read_sql(sql, conn)

print(time.time()-t)
