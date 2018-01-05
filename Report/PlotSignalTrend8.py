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

pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

conn = pymysql.connect("127.0.0.1","csuduan","715300","tools")
query='''
      select *
      from tools.signaldetail
      where strategy='StrategyTrend8' and ktype='M1' and product='jd'
      and date='20161014'   order by sysTms
'''

df = pd.read_sql(query, conn)
conn.close()
df['TradingTms']=df['Date']+' ' +df['Time']
df['ProfitRate']=df['ProfitAmt']/df['MarketValue'];
df['sumProfitRate'] = df['ProfitRate'].cumsum()

df['PriceRate']=df['Price'].pct_change()
df.loc[df.Instrument.str[-3:].apply(int).diff()!=0,'PriceRate']=0
df['sumPriceRate'] = df['PriceRate'].cumsum()

df['Sharp']= df.IndexVal.apply(lambda x: float(x.split(',')[0]))
df['Threshold']=df.IndexVal.apply(lambda x: float(x.split(',')[2]))
df['Stop']=df['Threshold']+df.IndexVal.apply(lambda x: float(x.split(',')[3]))




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
        y=df['Sharp'],
        name='Sharp',
        line=dict(width=1,dash='dash'),
        yaxis='y2'
    ),
    Scatter(
        x=df['TradingTms'],
        y=df['Threshold'],
        name='Threshold',
        line=dict(width=1,dash='dash'),
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







