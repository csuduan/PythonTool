#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 统计收益
import pymysql
import numpy as np
import pandas as pd




def stateFromCsv(file):
    df=pd.read_csv("D:\\CTA\\profitDiff\\profitdiff-20170421.csv")
    #df1=df[df["account"]=='宽投图灵']
    df1=df[df['account'].map(lambda x:x=="宽投图灵") & df['profittype']=='WIND']
    #df1=df[df['account'].isin('宽投图灵')]
    df2=pd.pivot_table(df1,values='profitamt',index='instrument',columns='strategy',aggfunc=np.sum)
    print(df2)


def stateFromMysql():
    sql=''' select * from tools.profit where  settledate='20170421'
    '''
    conn = pymysql.connect("127.0.0.1","csuduan","715300","tools",charset='utf8')
    df = pd.read_sql(sql, conn)
    conn.close()
    df1=df[(df['Account'].map(lambda x:x=="宽投图灵") )&( df['ProfitType']=="WIND")]
    df2=pd.pivot_table(df1,values='ProfitAmt',index='Instrument',columns='Strategy',aggfunc=np.sum)
    print(df2)



#主流程
try:
    pd.set_option('display.height',1000)
    pd.set_option('display.max_rows',500)
    pd.set_option('display.max_columns',500)
    pd.set_option('display.width',1000)
    #stateFromCsv()
    stateFromMysql()

except Exception as ex:
    print("Exception",ex)
    exit(-1)
