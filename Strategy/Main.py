#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Strategy.StrategyRsi import *
from Strategy.StrategyTrend1 import *
from Strategy.StrategyTrend2 import *
from Strategy.StrategyTrend3 import *
from Strategy.StrategyBo1 import *

from Strategy.KLineData import *
from xml.dom.minidom import parse
import xml.dom.minidom
import sys
import re
import logging
import sqlite3
import concurrent.futures
from datetime import datetime,timedelta


'''
Created on 2016年8月24日


@author: duanqing
'''
strategyConfigPath=r"E:\CTA\StrategyBatchInitConfig-ALL-TEST.xml"
kLinePath=r'E:\CTA\simulateMd\20160829'

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y%m%d %H:%M:%S',
                filename='myapp.log',
                filemode='w')




def runStrategy(strategy):
    strategy.Run()

if __name__ == '__main__':
    
    #连接sqlite
    sqliteConn=sqlite3.connect('../CTA.db3',check_same_thread = False)
    #检测表是否存在
    cursor = sqliteConn.execute(r"SELECT count(0) FROM sqlite_master WHERE type='table' AND name='KLINEDATA'")
    if cursor.fetchone()[0]==0 :
        print("未找到KLINEDATA!")
        sys.exit(1)
    cursor = sqliteConn.execute(r"SELECT count(0) FROM sqlite_master WHERE type='table' AND name='PROFIT'")
    if cursor.fetchone()[0]==0 :
        #不存在收益表，则新建表        
        sqliteConn.execute('''
        CREATE TABLE [PROFIT] (
        [SettleTms] TEXT  NULL,
        [SettleType] TEXT  NULL,
        [Strategy] TEXT  NULL,
        [Instrument] TEXT  NULL,
        [KType] TEXT  NULL,
        [Seq] TEXT  NULL,
        [SettleDate] TEXT  NULL,
        [Direction] TEXT  NULL,
        [IsTodayPosition] TEXT  NULL,
        [OpenTime] TEXT  NULL,
        [OpenPrice] REAL  NULL,
        [LastSettlePrice] REAL  NULL,
        [LastPrice] REAL  NULL,
        [Profit] REAL  NULL,
        [ProfitAmt] REAL  NULL
        );
        ''')
        print("创建表Profit完成")
    else:
        #情况profit
        sqliteConn.execute("delete FROM PROFIT")
        sqliteConn.commit()
    

    print("===>开始执行策略。。。")
    
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    
    try: 

        
        dom = xml.dom.minidom.parse(strategyConfigPath)
        root = dom.documentElement
        strategyConfigs = root.getElementsByTagName("StrategyBatchInitConfig")
        
        startTime=datetime.now()
        for config in strategyConfigs:
            strategyType=config.getAttribute("StrategyType")
            instrument=config.getAttribute("Instrument")
            intervalType=config.getAttribute("IntervalType")
            offset=config.getAttribute("TradeTimeOffset")
            volume=config.getAttribute("TargetVolume")   
            configPath=config.getAttribute("InitConfigFilePath")
            
            if strategyType!="StrategyRsi1":
                strategy=globals()[strategyType](instrument,intervalType,offset,volume,configPath,sqliteConn)
                #executor.submit(runStrategy,strategy) 
                runStrategy(strategy)
            else:
                product=re.sub(r'\d',"",instrument)
                cursor=sqliteConn.execute("select * from MAINFORCEMAPPING WHERE PRODUCT = '{0}'".format(product))
                for row in cursor:
                    strategy=globals()[strategyType](row[0],intervalType,offset,volume,configPath,sqliteConn)
                    #executor.submit(runStrategy,strategy) 
                    runStrategy(strategy)    
        cost=datetime.now()-startTime
        #print("===>全部执行完毕，总耗时{0}".format(cost.seconds))
        
    except(Exception) as ex:
        print ("解析配置文件失败",ex)    
        sys.exit(1) 
        
    #sqliteConn.close()
    

else:
    print("222")
    
