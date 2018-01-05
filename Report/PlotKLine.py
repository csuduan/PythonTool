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
product='j'
type='D1'
start='20160000'
sql=f'''
    select * from (select * from tools.klinedata where Date>'{start}' and Product='{product}'  and type='{type}') a
    inner join tools.mainforcemapping b
    on (a.Instrument = b.instrumentID and a.Date>=b.StartDate && a.Date<=b.EndDate )
    order by a.Systms;
    '''
df = pd.read_sql(sql, conn)

df['Rate']=df['ClosePrice'].pct_change()
df.loc[df.Instrument.str[-3:].apply(int).diff()!=0,'Rate']=0

df['SumRate']=df['Rate'].cumsum()
df['Tms']=df['Date']+' '+df['Time']

#计算Sharp
sharp =df['Rate'].mean()/df['Rate'].std()
print(sharp)



data=[
    Scatter(
        x=df['Tms'],
        y=df['ClosePrice'],
        name='Price',
        yaxis='y2'

        #text=country_names,
        #mode='markers'
    ),
    Scatter(
        x=df['Tms'],
        y=df['SumRate'],
        name='PriceRate',
        text=df['Instrument'],
        yaxis='y1'

        #text=country_names,
        #mode='markers'
    ),


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







