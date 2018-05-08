
# -*- coding:utf-8 -*-
import re
from lxml import etree
import requests
import pandas as pd
import sqlalchemy
import time

#外汇中间价爬虫

url = 'http://www.boc.cn/sourcedb/whpj/index.html'  # 网址
r=requests.get(url)
print(r.status_code,r.encoding)
html = r.content.decode('utf-8')


currencys={'USD':'美元',
           'JPY':'日元',
           'EUR':'欧元',
           'GBP':'英镑',
           'HKD':'港币',
           'KER':'韩国元',
           'AUD':'澳大利亚元',
           'CAD':'加拿大元'}

engine =sqlalchemy.create_engine('mssql+pymssql://wind:wind@192.168.1.10:1433/wind')
data=[]
for currencyCh,currencyEn in currencys.items():
    a = html.index(f'<td>{currencyEn}</td>')  # 取得“新西兰元”当前位置
    s = html[a:a + 300]  # 截取新西兰元汇率那部内容（从a到a+300位置）
    result = re.findall('<td>(.*?)</td>', s)  # 正则获取
    result.append(currencyCh)
    data.append(result)

df=pd.DataFrame(data)
df1=df.iloc[:,[8,6,5]]
df1.columns=['CRNCY_CODE','TRADE_DT','CRNCY_MIDRATE']


today=time.strftime('%Y%m%d',time.localtime(time.time()))

try:
    engine.connect().execute(f'delete from FXRMBMIDRATE where TRADE_DT=\'{today}\'')
except Exception as ex:
    print(ex)


tms=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
df1['TRADE_DT']=df1['TRADE_DT'].apply(lambda x:x[0:4]+x[5:7]+x[8:10])
df1['OPDATE']=tms
df1['OBJECT_ID']=0
df1['CRNCY_MIDRATE']=df1['CRNCY_MIDRATE'].apply(lambda  x:round((float)(x)/100,6))
df1['OPMODE']=0
print(df1)
df1.to_sql('FXRMBMIDRATE',engine,index=False,if_exists='append')

# 方式二：lxml获取
# result=etree.HTML(html).xpath('//table[@cellpadding="0"]/tr[18]/td/text()')

