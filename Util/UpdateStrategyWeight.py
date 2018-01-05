import numpy as np
import pandas as pd
import sqlalchemy
import time

#更新策略权重配置脚本

configFile='D:\SVN\Quantinv\策略\策略交易配置\CTA产品\Trend策略配比-V2.xlsx'

config=config=pd.read_excel(configFile,sheetname='Trend-N1')

print(config)
strategys=config.columns[1:]

engine =sqlalchemy.create_engine('mssql+pymssql://duanqing:duanqing@192.168.1.10:1433/Strategy')
sql='select * from [Strategy].[dbo].[StrategyInfo] where Owner=\'段晴\''
strategyInfo=pd.read_sql(sql,engine)

result=None;
tms=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
lastday='20170811'
today='20170814'
for s in strategys:
    strategy,type=s.split('_')
    desc=strategy+'-'+type.upper()
    info=strategyInfo.loc[strategyInfo['StrategyDesc']==desc]
    straegyId=info['StrategyID'].values[0]

    tmp=config[config[s].notnull()].copy()
    if len(tmp) ==0:
        continue
    #tmp=config.loc[:,['product',s]]
    sum=tmp.loc[:,s].sum()
    tmp['Weight']=tmp[s]/sum
    tmp['Contract']=tmp['product'].apply(lambda  x:x.upper())


    tmp=tmp.loc[:,['Contract','Weight']]

    tmp['StrategyId']=straegyId
    tmp['ParamType']=0
    tmp['StartDate']=today
    tmp['EndDate']='21000101'
    tmp['EndDate']='21000101'
    tmp['OPDATE']=tms

    #先删除新录入的
    engine.connect().execute(f'delete from StrategyWeight where strategyId=\'{straegyId}\' and startDate=\'{today}\'')
    #更新之前的
    engine.connect().execute(f'update  StrategyWeight set enddate=\'{lastday}\' where strategyId=\'{straegyId}\' and  endDate=\'21000101\'')
    tmp.to_sql('StrategyWeight',engine,index=False,if_exists='append')
    pass








