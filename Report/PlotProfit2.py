#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 信号明细绘图

import sys
import pymysql
import time
import os
import shutil
import re

import string
import numpy as np
import pandas as pd

import plotly
from plotly.graph_objs import *

def convertDirection(direction):
    if direction == 'Long':
        return  0.01
    elif direction == "Short":
        return -0.01
    else:
        return 0;

marketValue=1000000

conn = pymysql.connect("127.0.0.1","csuduan","715300","tools",charset='utf8')
query='''select concat(SettleDate,' 00:00:00') as Date ,MarketValue,ProfitAmt,Product
            from tools.profit where  account='STD' and profitType='WIND' and strategy='StrategyTrend2'   and ktype='M5' and Settledate >'20170000'
    '''

df = pd.read_sql(query, conn,)
conn.close()
df = df.sort_values(by='Date');
#df=df.loc[df['MarketValue']!=0]
df['ProfitRate']=df['ProfitAmt']/df['MarketValue']
print(df[df['Product']=='a'])

#df=df.pivot_table(index='Date', columns='Product',values='ProfitRate').cumsum().dropna(axis=1, how='all')
df1=df.pivot_table(index='Date', columns='Product',values='ProfitRate',aggfunc=np.sum)
df2=df1.cumsum()

#df=df.groupby('Date').agg({'ProfitAmt':'sum','MarketValue':'last'})
#df['Date']=df.index

#df['sumPriceRate'] = df['LastPrice'].pct_change().cumsum()

#df['sumProfitRate'] = df['ProfitRate'].cumsum()


data=[]
for col in df2.columns:
    data.append(Scatter(x = df2.index, y = df2[col], name = col))

#url=plotly.offline.plot( data,Layout(title="收益表现"),filename='plot-华二二trend2-M5.html',auto_open=False)
url=plotly.offline.plot( data,Layout(title="收益表现"),filename='plot-华二二trend2-M5.html')








