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

import PdFormat

from Dao.MainForceDao import  *



#读取数据

# df=pd.read_csv('D:\\CTA\\A-position.csv')
# df = df.dropna(subset=['名次'])
#
# # print(time.clock())
# a = time.time()
# #计算ITS
# for name,datas in df.groupby('日期'):
#     # print(datas)
#     pass
#     tmp = datas[['成交量', '多单量','空单量']].rank(method='dense', ascending=False)
#     tmp.columns=['rank1', 'rank2', 'rank3']
#     datas = pd.concat([datas, tmp], axis=1)
#     result=datas.loc[(datas.rank1 < 20) & (datas.rank2 < 20) &(datas.rank3<20)]
#
#     #result['rate']=(result.多单量+result.空单量)/result.成交量
#     avg=((result.多单量+result.空单量)/result.成交量).mean()
#     result=result.loc[((result.多单量+result.空单量)/result.成交量)>avg]
#     its=(result.多单量.sum()-result.空单量.sum())/(result.多单量.sum()+result.空单量.sum())
#     #print(0)
#
#     pass
# # print(time.clock())
#
# print(time.time() - a)
#
#
# #处理数据
#
# dfMainForce=MainForceDao.QryMainForce('a')
# for mainForce in dfMainForce:
#
#     pass;
#
# print('End')


product='ag'



def its():
    dfMainForce=MainForceDao.QryMainForce('a')
    pass

if __name__ == '__main__':
    its()