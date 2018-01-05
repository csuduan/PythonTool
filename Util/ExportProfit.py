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

account='STD'
date=time.strftime('%Y%m%d',time.localtime(time.time()))
conn = pymysql.connect("127.0.0.1","csuduan","715300","tools",charset='utf8')
sql=f'''
  select * from tools.profit
  where account='{account}' and profitType='WIND'  and settledate>'20160000'
'''
df = pd.read_sql(sql, conn)
path=f"D:\\CTA\\export\\profit-{account}-{date}.csv"
df.to_csv(path)
#打开文件
os.system(path)


#table=df.pivot_table(index='SettleDate', columns=['Strategy','KType'],values='ProfitAmt',aggfunc=np.sum)
#print(table)