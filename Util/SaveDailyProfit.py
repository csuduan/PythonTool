# -*- coding:utf-8 -*-
import pandas as pd
import sqlalchemy
import time
import os
import sqlalchemy
# author : duanqing

#保存每日收益到数据库

path='D:\SVN\svn-Aliyun\收益记录'
encoding='cp936'
#startDate='20180201'
startDate=time.strftime('%Y%m%d',time.localtime(time.time()))
tms=time.strftime('%Y%m%d %H:%M:%S',time.localtime(time.time()))



engine =sqlalchemy.create_engine('mssql+pymssql://quant:quant@192.168.1.10:1433/product?charset=cp936')

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

products=pd.read_sql("select * from productNameData",engine)


print('开始更新svn')
os.system('svn up ' +path)

print(f'开始装载{startDate}起的收益文件')

l=list()

def parseFile(filePath,account,productId):
    file =open(filePath,'r',encoding='utf-8')
    for line in file:
        if line.count('平仓结算')==0 and line.count("持仓结算")==0:
            continue

        datas=line.split('\t')

        if  datas[4] < startDate:
            continue


        dic=dict()

        dic['ProductId']=int(productId)
        dic['Account']=account
        dic['SettleType']=datas[1]
        dic['StrategyId']=datas[2]
        dic['StrategyType']=datas[3]
        dic['KType']=dic['StrategyId'].split('-')[2]
        dic['TradingDay']=datas[4]
        dic['Contract']=datas[5]
        dic['PositionType']=('TdPosition' if datas[6]=='True' else 'YdPosition')
        dic['Direction']=datas[7]
        dic['Volume']=int(datas[8])
        dic['Commission']=float(datas[9])
        dic['LastPrice']=float(datas[10])
        lastSettlePrice=datas[11]
        dic['AvgPrice']=float(datas[12])
        dic['ProfitPoint']=float(datas[15])
        dic['ProfitAmt']=float(datas[16])
        dic['OpenTime']=datas[17]
        dic['OpTms']=tms


        l.append(dic)



for subDir in os.listdir(path):
    subPath=path+'\\'+subDir
    account=subDir
    product=products[products.ProductName==subDir]
    if len(product) ==0:
        print(f'账户[{account}]找不到对应product信息')
        continue
    productId=product.iloc[0,1]
    for file in os.listdir(subPath):
        filePath=subPath+'\\'+file
        parseFile(filePath,account,productId)


    print(f'''装载账户:{account} 完成''')

df=pd.DataFrame(l)

print("开始入库")
try:
    engine.connect().execute(f'delete from FuturesSettleData where TradingDay>=\'{startDate}\'')
    writeables=df.applymap(lambda  x:str(x).encode(encoding) if  x==x else None)
    writeables.to_sql('FuturesSettleData',engine,index=False,if_exists='append')

except Exception as ex:
    print(ex)

print("装载完毕")






