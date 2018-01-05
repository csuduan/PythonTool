
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 计算最大回撤


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

marketValue=6000000
conn = pymysql.connect("127.0.0.1","csuduan","715300","tools",charset='utf8')
query='''select  concat(settledate,'00:00:00:00') as date,sum(profitAmt) as profit  from tools.profit
         where  account='STD' and profitType='WIND' and settledate>'20170000' and strategy='StrategyTrend1' 
         group by settledate'''

try:
    df = pd.read_sql(query, conn)
    conn.close()
    #计算最大回撤
    df = df.sort('date')
    df['profitRate']=df['profit']/marketValue
    df['sumProfitRate']=df['profitRate'].cumsum()
    df['drawDown']=df['sumProfitRate'].cummax()-df['sumProfitRate']

except Exception as ex:
    print("Exception",ex)
    exit(-1)

data=[
    Scatter(
        x=df['date'],
        y=df['drawDown'],
        name='drawDown'

    ),


]

url=plotly.offline.plot( data,Layout(title="最大回撤曲线"),filename='plot.html')
print(url)