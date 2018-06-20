
import pandas as pd
import datetime
import sqlalchemy
import numpy as np
from line_profiler import LineProfiler

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

engine =sqlalchemy.create_engine('mssql+pymssql://quant:quant@192.168.1.10:1433/TuShare?charset=cp936')

# inner='CU'
# foreign='CAD'
# tickInner=25
# tickForeign=1

inner='NI'
foreign='NID'
tickInner=10
tickForeign=5

def GetDatas():
    sql1=f"select date,time,closeprice from [ForeignFuturesMinutePrice] where contract='{inner}' and date>='20170101' and date<'20180101' and type=1 "
    sql2=f"select date,time,closeprice from [ForeignFuturesMinutePrice] where contract='{foreign}' and date>='20170101' and date<'20180101' and type=1 "
    sqlfx="select trade_dt as date, CRNCY_MIDRATE as fx from [WIND].[db_datareader].[FXRMBMIDRATE] where CRNCY_CODE='USD' "

    df1=pd.read_sql(sql1,engine)
    df2=pd.read_sql(sql2,engine)
    dffx=pd.read_sql(sqlfx,engine)

    df=df1.merge(df2,how='outer',on=['date','time'])
    df=df.merge(dffx,how='left',on=['date'])
    df['datetime']=df.date+' '+df.time
    df=df.sort_values(by=['date','time'])

    #筛选有效交易时间
    df=df[(df.time>='09:00:00')&(df.time<='10:15:00')|
          (df.time>='10:15:00')&(df.time<='11:30:00')|
          (df.time>='13:30:00')&(df.time<='15:00:00')|
          (df.time>='21:00:00')|
          (df.time<='01:00:00')]

    df=df.fillna(method='pad')

    return  df




def strategy(df):
    signal = 0
    listSignal=[0]
    listOper=[0]
    for i in range(1,len(df)):
        row = df.iloc[i]
        lastrow=df.iloc[i-1]

        newsig = signal
        oper=0

        if row.Y < openpct * row.STD + row.MEAN  and \
                lastrow.Y > openpct * lastrow.STD + lastrow.MEAN and signal == 0:
            newsig = -1
            oper=1

        if row.Y < -closepct * row.STD + row.MEAN and signal == -1:
            newsig = 0
            oper = 1

        if row.Y > -openpct * row.STD + row.MEAN and \
                lastrow.Y < -openpct * lastrow.STD + lastrow.MEAN  and signal == 0:
            newsig = 1
            oper = 1

        if row.Y > closepct * row.STD + row.MEAN and signal == 1:
            newsig = 0
            oper = 1

        signal = newsig
        listSignal.append(signal)
        listOper.append(oper)

    df['Oper'] = listOper
    df['Signal'] = listSignal
    df['Position']=df['Signal'].shift(1)
    return  df



if __name__ == "__main__":
    df=GetDatas()
    x=24000
    openpct=2
    closepct=1.5


    df['Y']=df.closeprice_x / (df.closeprice_y*df.fx)
    df['STD']=df.Y.rolling(window=x,min_periods=1).std()
    df['MEAN'] = df.Y.rolling(window=x,min_periods=1).mean()

    #策略逻辑
    df=strategy(df)

    #计算收益
    df['last_closeprice_x']=df['closeprice_x'].shift(1)
    df['last_closeprice_y'] = df['closeprice_y'].shift(1)


    df['profit_x']=((df.closeprice_x-df.last_closeprice_x)*df.Position-df.Oper*tickInner*1)/df.last_closeprice_x
    df['profit_y'] = ((df.closeprice_y - df.last_closeprice_y) * df.Position*-1-df.Oper*tickForeign*df.fx*1)/df.last_closeprice_y
    df['profit']=((df.closeprice_x-df.last_closeprice_x)*df.Position+(df.closeprice_y - df.last_closeprice_y) * df.Position*-1-df.Oper*tickInner*1-df.Oper*tickForeign*df.fx*1)/(df.last_closeprice_x+df.last_closeprice_y)

    df['sumProfit_x']=df['profit_x'].cumsum()
    df['sumprofit_y'] = df['profit_y'].cumsum()
    df['sumprofit'] = df['profit'].cumsum()


    #画图
    df.plot(x='datetime', y=['sumProfit_x', 'sumprofit_y', 'sumprofit'])



    pass