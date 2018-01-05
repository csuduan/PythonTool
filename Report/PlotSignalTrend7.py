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
import  numpy as np


import plotly
from plotly.graph_objs import *

pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

conn = pymysql.connect("127.0.0.1","csuduan","715300","tools")
query='''
      select *
      from tools.signaldetail
      where strategy='StrategyTrend7' and ktype='M1' and product='ru'
      and date='20160324'    order by sysTms
'''

df = pd.read_sql(query, conn)
conn.close()
df['TradingTms']=df['Date']+' ' +df['Time']
df['ProfitRate']=df['ProfitAmt']/df['MarketValue'];
df['sumProfitRate'] = df['ProfitRate'].cumsum()

df['PriceRate']=df['Price'].pct_change()
df.loc[df.Instrument.str[-3:].apply(int).diff()!=0,'PriceRate']=0
df['sumPriceRate'] = df['PriceRate'].cumsum()

df['LongVolatility']= df.IndexVal.apply(lambda x: float(x.split(',')[0]))
df['ShortVolatility']= df.IndexVal.apply(lambda x: float(x.split(',')[1]))
#df['DiffVolatility']= df.IndexVal.apply(lambda x: float(x.split(',')[2]))
df['Threshold']=df.IndexVal.apply(lambda x: float(x.split(',')[3]))
df['Variance']=df.IndexVal.apply(lambda x: float(x.split(',')[4]))*10

df['LongVariance']=df['LongVolatility']/df['Variance']/10
df['ShortVariance']=df['ShortVolatility']/df['Variance']/10

df['Diff']=(df['ShortVolatility']-df['LongVolatility'])
df['Diff1']=df.Diff.ewm(alpha=2/21).mean()

df['Diff2']=df.Diff.ewm(alpha=2/11).mean()






data=[
    Scatter(
        x=df['TradingTms'],
        y=df['sumPriceRate'],
        name='PriceRate',
        text=df['Instrument']


        #text=country_names,
        #mode='markers'
    ),
    Scatter(
        x=df['TradingTms'],
        y=df['sumProfitRate'],
        name='ProfitRate',
        text=df['Direction'],

        yaxis='y'
    ),


    Scatter(
        x=df['TradingTms'],
        y=df['ShortVolatility'],
        name='ShortVolatility',
        line=dict(width=1,dash='dash'),
        yaxis='y2'
    ),
    Scatter(
        x=df['TradingTms'],
        y=df['LongVolatility'],
        name='LongVolatility',
        line=dict(width=1,dash='dash'),
        yaxis='y2'
    ),
    # Scatter(
    #     x=df['TradingTms'],
    #     y=df['Threshold'],
    #     name='Threshold',
    #     line=dict(width=1,dash='dash'),
    #     yaxis='y2'
    # ),
    #
    # Scatter(
    #     x=df['TradingTms'],
    #     y=df['ShortVariance'],
    #     name='ShortVariance',
    #     line=dict(width=1,dash='dash'),
    #     yaxis='y2'
    # ),
    # Scatter(
    #     x=df['TradingTms'],
    #     y=df['LongVariance'],
    #     name='LongVariance',
    #     line=dict(width=1,dash='dash'),
    #     yaxis='y2'
    # ),
    # Scatter(
    #     x=df['TradingTms'],
    #     y=df['Variance'],
    #     name='Variance',
    #     line=dict(width=1,dash='dash'),
    #     yaxis='y2'
    # ),
    Scatter(
        x=df['TradingTms'],
        y=df['Diff'],
        name='Diff',
        line=dict(width=1,dash='solid'),
        yaxis='y2'
    ),
    Scatter(
        x=df['TradingTms'],
        y=df['Diff1'],
        name='Diff1',
        line=dict(width=1,dash='solid'),
        yaxis='y2'
    ),
    Scatter(
        x=df['TradingTms'],
        y=df['Diff2'],
        name='Diff2',
        line=dict(width=1,dash='solid'),
        yaxis='y2'
    ),
    # Scatter(
    #     x=df['TradingTms'],
    #     y=df['Stop'],
    #     name='Stop',
    #     line=dict(width=1,dash='dash'),
    #     yaxis='y2'
    # )

]
layout=Layout(
    title='SignalDetail',
    yaxis=dict(
        title='变化率'
    ),
    yaxis2=dict(
        title='信号',
        titlefont=dict(
            color='rgb(148, 103, 189)'
        ),
        tickfont=dict(
            color='rgb(148, 103, 189)'
        ),
        overlaying='y',
        side='right'
    ),


)
url=plotly.offline.plot(Figure(data=data,layout=layout),filename='plot.html')
print(url)







