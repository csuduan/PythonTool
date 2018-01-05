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

account='TestTrend3'
strategy='StrategyTrend3'
ktype='D1'
product='ru'

pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

conn = pymysql.connect("127.0.0.1","csuduan","715300","tools",charset='utf8')

query=f'''select * from tools.profit
        where  account='{account}' and profittype='WIND'
        and strategy='{strategy}' and ktype='{ktype}' and product='{product}'
        and Settledate >'20160000'
        order by SettleDate

        '''
title=f'{strategy}-{ktype}-{product}'

df = pd.read_sql(query, conn,)
#df = df.sort_values(by='Date')


#合并平仓结算收益

df['profitRate']=df['ProfitAmt']/df['MarketValue']
df1=df.groupby('SettleDate').agg({'profitRate':'sum'})
df1['sumProfitRate'] = df1['profitRate'].cumsum()

df2=df[df['SettleType']=='持仓结算']
df2['priceRate']=(df2['LastPrice']-df2['LastSettlePrice'])/df2['LastSettlePrice']
#df2['priceRate']=
df2['sumPriceRate'] = df2['priceRate'].cumsum()
df2.index=df2.SettleDate

df = pd.concat([df1, df2], axis=1)
df['Date']=df['SettleDate']+'A'

data=[
    Scatter(
        x=df['Date'],
        y=df['sumPriceRate'],
        name='PriceRate',
        text=df['Instrument']

        #text=country_names,
        #mode='markers'
    ),
    Scatter(
        x=df['Date'],
        y=df['sumProfitRate'],
        text=df['Direction'],
        name='ProfitRate',
        # mode = 'lines+markers',
        # line=dict(color=('rgb(205,12,24)'),width=1,dash='solid'), # dash options include 'dash', 'dot', and 'dashdot'
        # marker=dict(color='rgba(67,67,67,1)',size=2),
        #yaxis='y2'
    )


]

url=plotly.offline.plot( Figure(data=data,layout=Layout(title=title)),filename='..\out\plot.html')
print(url)







