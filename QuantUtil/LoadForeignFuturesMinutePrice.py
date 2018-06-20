#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: duanqing
# @created on: 2018/5/7 13:24
# @desc  : 装载外盘期货日行情数据

import pandas as pd
import datetime
import sqlalchemy

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

sourcePath='D:\\User\\csuduan\\桌面\\外盘数据\\东方宽客1分钟线数据'
engine =sqlalchemy.create_engine('mssql+pymssql://quant:quant@192.168.1.10:1433/DBFUTURESMINIUTEPRICES?charset=cp936')
engineU =sqlalchemy.create_engine('mssql+pymssql://quant:quant@192.168.1.10:1433/TuShare')


def loadForeignEodPrice(contract):
    '''外盘日行情'''
    df = pd.read_csv(f'{sourcePath}\\{contract} 主力 1分钟线本地时间.txt', engine='python')
    #df['Date']=df['Date'].str.replace('-','')



    df2 = pd.DataFrame()
    df2['Date'] = df['Date'].str.replace('-','')
    df2['Time'] = df['Time']
    df2['Contract'] = contract.split(' ')[1]
    df2['Exchange'] = contract.split(' ')[0]
    df2['OpenPrice'] = df['Open']
    df2['ClosePrice'] = df['Close']
    df2['HighPrice'] = df['High']
    df2['LowPrice'] = df['Low']
    df2['Volume'] = df['TotalVolume']
    df2['OpTms'] = datetime.datetime.now()
    df2['Type']=1







    # 写数据
    engineU.execute(f"delete from ForeignFuturesMinutePrice where Contract='{contract.split(' ')[1]}' ")
    df2.to_sql('ForeignFuturesMinutePrice', engineU, index=False, if_exists='append')

def loadInnerEodPrice(contract):
    '''内盘日行情'''
    sql = f"select * from [DBFUTURESMINIUTEPRICES].[dbo].[{contract.split('.')[0]}] where  TRADE_DT>'20160101' and S_INFO_WINDCODE='{contract}' and DATATYPE=1 and S_DQ_VOLUME>0"
    df = pd.read_sql(sql, engine)

    df=df.sort_values(by='DATETIME')


    df2 = pd.DataFrame()
    df2['Date'] = df['TRADE_DT_N']
    df2['Time'] = df['TIMEOFDAY']
    df2['Contract'] = contract.split('.')[0]
    df2['Exchange'] = contract.split('.')[1]
    df2['OpenPrice'] = df['S_DQ_OPEN']
    df2['ClosePrice'] = df['S_DQ_CLOSE']
    df2['HighPrice'] = df['S_DQ_HIGH']
    df2['LowPrice'] = df['S_DQ_LOW']
    df2['Volume'] = df['S_DQ_VOLUME']
    df2['OpTms'] = datetime.datetime.now()
    df2['Type'] = 1


    # 写数据
    engineU.execute(f"delete from ForeignFuturesMinutePrice where Contract='{contract.split('.')[0]}' ")
    df2.to_sql('ForeignFuturesMinutePrice', engineU, index=False, if_exists='append')

if __name__ == "__main__":
    contractList=['LME NID']
    for contract in contractList:

        try:
            loadForeignEodPrice(contract)
            print(f'load  {contract} success')
        except Exception as ex:
            print(f'load  {contract} error:{ex}')

    contractList = ['NI.SHF']

    for contract in contractList:

        try:
            loadInnerEodPrice(contract)
            print(f'load  {contract} success')
        except Exception as ex:
            print(f'load  {contract} error:{ex}')

