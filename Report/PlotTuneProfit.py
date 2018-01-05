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


conn = pymysql.connect("127.0.0.1","csuduan","715300","tools")
query='''select concat(date,' 00:00:00') as Date ,PriceRate,ProfitRate,Direction
                from tools.tunedayprofit where  product='IF' and date >'20160000' order by date
        '''
df = pd.read_sql(query, conn)
conn.close()

df = df.sort(['Date'], ascending=[1]);
df['sumPriceRate'] = df['PriceRate'].cumsum()
df['sumProfitRate'] = df['ProfitRate'].cumsum()
df['dir'] = df['Direction'].apply(lambda  x:convertDirection(x))



data=[
    Scatter(
        x=df['Date'],
        y=df['sumPriceRate'],
        name='PriceRate'

        #text=country_names,
        #mode='markers'
    ),
    Scatter(
        x=df['Date'],
        y=df['sumProfitRate'],
        name='ProfitRate',
        mode = 'lines+markers',
        #mode = 'lines',
        line=dict(color=('rgb(205,12,24)'),width=1,dash='solid'), # dash options include 'dash', 'dot', and 'dashdot'
        marker=dict(color='rgba(67,67,67,1)',size=2),
        #yaxis='y2'
    ),
    Bar(
        x=df['Date'],
        y=df['dir'],
        name='direction'
    )


]

url=plotly.offline.plot( data,Layout(title="hello world"),filename='plot.html')
print(url)







