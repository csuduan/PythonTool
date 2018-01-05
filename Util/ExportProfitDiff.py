#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 导出收益差

import sys
import time

import pymysql
import os
import shutil
import re

import string
import numpy as np
import pandas as pd
import datetime

import plotly
from plotly.graph_objs import *

#date=time.strftime("%Y%m%d",time.localtime(time.time()))
date=datetime.datetime.now().strftime("%Y%m%d")

#date='20170525'
account='阳月三号'



conn = pymysql.connect("127.0.0.1","csuduan","715300","tools",charset='utf8')
sql=f'''
  select * from tools.profit
  where SettleDate='{date}' and account='{account}'  order by StrategyId
'''
df = pd.read_sql(sql, conn)
conn.close()

df.to_csv(f"..\out\\profitDiff.csv")
os.system("..\out\\profitDiff.csv")
#os.system("explorer.exe %s" % '..\out')
