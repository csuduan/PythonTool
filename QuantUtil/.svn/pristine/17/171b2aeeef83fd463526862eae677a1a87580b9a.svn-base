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
    df['LastTime'] = df['Time'].shift()
    df['Flg']=0
    df.loc[(df.LastTime <= '14:30:00') & (df.Time > '14:30:00'), 'Flg'] = 1
    df['SumFlg']=df['Flg'].cumsum()


    grouped = df.groupby(['SumFlg'])
    df2 = pd.DataFrame()
    df2['Date'] = grouped['Date'].last().str.replace('-','')
    df2['Time'] = grouped['Time'].last()
    df2['Contract'] = contract.split(' ')[1]
    df2['Exchange'] = contract.split(' ')[0]
    df2['OpenPrice'] = grouped['Open'].first()
    df2['ClosePrice'] = grouped['Close'].last()
    df2['HighPrice'] = grouped['High'].max()
    df2['LowPrice'] = grouped['Low'].min()
    df2['Volume'] = grouped['TotalVolume'].sum()
    df2['OpTms'] = datetime.datetime.now()




    # 写数据
    engineU.execute(f"delete from ForeignFuturesEodPrice where Contract='{contract.split(' ')[1]}' ")
    df2.to_sql('ForeignFuturesEodPrice', engineU, index=False, if_exists='append')


def loadInnerEodPrice(contract):
    '''内盘日行情'''
    sql = f"select * from [DBFUTURESMINIUTEPRICES].[dbo].[{contract.split('.')[0]}] where  TRADE_DT>'20160101' and S_INFO_WINDCODE='{contract}' and DATATYPE=1 and S_DQ_VOLUME>0"
    df = pd.read_sql(sql, engine)

    df=df.sort_values(by='DATETIME')

    df['LastTime'] = df['TIMEOFDAY'].shift()
    df['Flg'] = 0
    df.loc[(df.LastTime <= '14:30:00') & (df.TIMEOFDAY > '14:30:00'), 'Flg'] = 1
    df['SumFlg'] = df['Flg'].cumsum()

    grouped = df.groupby(['SumFlg'])
    df2 = pd.DataFrame()
    df2['Date'] = grouped['TRADE_DT_N'].last()
    df2['Time'] = grouped['TIMEOFDAY'].last()
    df2['Contract'] = contract.split('.')[0]
    df2['Exchange'] = contract.split('.')[1]
    df2['OpenPrice'] = grouped['S_DQ_OPEN'].first()
    df2['ClosePrice'] = grouped['S_DQ_CLOSE'].last()
    df2['HighPrice'] = grouped['S_DQ_HIGH'].max()
    df2['LowPrice'] = grouped['S_DQ_LOW'].min()
    df2['Volume'] = grouped['S_DQ_VOLUME'].sum()
    df2['OpTms'] = datetime.datetime.now()

    df2=df2[:-1]

    # 写数据
    engineU.execute(f"delete from ForeignFuturesEodPrice where Contract='{contract.split('.')[0]}' ")
    df2.to_sql('ForeignFuturesEodPrice', engineU, index=False, if_exists='append')


if __name__ == "__main__":
    contractList=['LME AHD','LME CAD','LME NID','LME PBD','LME SND','LME ZSD']
    for contract in contractList:

        try:
            loadForeignEodPrice(contract)
            print(f'load  {contract} success')
        except Exception as ex:
            print(f'load  {contract} error:{ex}')

    contractList = ['CU.SHF','AL.SHF','ZN.SHF']
    for contract in contractList:

        try:
            loadInnerEodPrice(contract)
            print(f'load  {contract} success')
        except Exception as ex:
            print(f'load  {contract} error:{ex}')

