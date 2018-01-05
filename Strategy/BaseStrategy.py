'''
Created on 2016年8月24日

@author: duanqing
'''
from Strategy.KLineData import *
from datetime import datetime,timedelta
import Strategy.Utils
import re
import logging
import sqlite3

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] %(message)s',
                datefmt='%Y%m%d %H:%M:%S',
                filename='myapp.log',
                filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s][%(name)-8s] [%(levelname)-5s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class BaseStrategy(object):
    '''
    classdocs
    '''
    Instrument=""
    IntervalType=""
    TradeTimeOffset=0
    TargetVolume=0
    InitConfigFilePath=""
    tradeTime=None

    
    order=None
    
   
    def __init__(self,instrment,intervalType,offSet,volume,configPath,sqliteConn=None):
        '''
        Constructor
        '''
        self.profitList=[]
        self.kLineDatas=[]
        self.Instrument=instrment
        self.IntervalType=intervalType
        self.TargetVolume=volume
        self.InitConfigFilePath=configPath
        self.tradeTime=Strategy.Utils.GetTradeTime(self.Instrument)
        self.sqliteConn=sqliteConn
        self.ProfitList=[]

    
    def Run(self):
        #self.sqliteConn=sqlite3.connect('../CTA.db3',check_same_thread = False)
        startTime=datetime.now()
        logging.info("执行策略{0} {1}...".format(self.__class__.__name__,self.GetStrategyName()))
        try:
            if self.LoadParam()==0:
                #装载KLine并执行策略
                self.LoadKLine()
                cost=datetime.now()-startTime
                logging.info("执行策略{0} {1}成功  耗时{2}s".format(self.__class__.__name__,self.GetStrategyName(),cost.seconds))
            else:
                logging.error("装载参数文件失败")
        except Exception as ex:
            logging.error("执行策略遇到异常")
            logging.exception(ex)
        
        for data in self.ProfitList:
            self.sqliteConn.execute("INSERT INTO PROFIT VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",data)
        self.sqliteConn.commit()    
        #self.sqliteConn.close()
            
    def GetStrategyName(self):
        return "{0}-{1}-{2}".format(self.Instrument,self.IntervalType,self.TradeTimeOffset)
    
    def Algorithm(self,kLinedata):
        pass
    
    def LoadParam(self):
        f=None
        paramDic={}
        try:
            f=open(self.InitConfigFilePath,'r',encoding= 'UTF-8')
            for line in f:
                match=re.match( r'\[(.*)\].*=(.*)', line, re.M|re.I)
                if match:
                    paramDic[match.group(1).strip()]=   match.group(2).strip()
                    if hasattr(self, match.group(1).strip()):
                        tmp=getattr(self,match.group(1).strip())
                        if isinstance(tmp, bool):
                            if match.group(2).strip()=="True" or match.group(2).strip()=="true":
                                setattr(self,match.group(1).strip(),True) 
                            else:
                                setattr(self,match.group(1).strip(),False) 
                        elif isinstance(tmp, int):
                            setattr(self,match.group(1).strip(),int(match.group(2).strip()))
                        elif isinstance(tmp, float):
                            setattr(self,match.group(1).strip(),float(match.group(2).strip()))
                            
                        else:
                            setattr(self,match.group(1).strip(),match.group(2).strip())
                                               
        except(Exception) as ex:
            print("解析参数文件失败",self.InitConfigFilePath,ex)
            return -1    
        f.close()        
        
        return 0
    
    def LoadKLine(self):
        #print("Load ...",file)
        
        lastDate=None
        f=None
        try:
            sql=r"select * from KLINEDATA WHERE INSTRUMENT='{0}' AND TYPE='{1}'".format(self.Instrument,self.IntervalType)
            cursor =self.sqliteConn.execute(sql)
            #data=cursor.fetchall()
            for row in cursor:
                kLineData=KLineData()
                kLineData.instrumentId=self.Instrument
                kLineData.type=self.IntervalType
                kLineData.offset=self.TradeTimeOffset
                
                kLineData.tms=datetime.strptime(row[2]+" "+row[3],'%Y%m%d %H:%M:%S') 
                kLineData.openPrice=row[4]
                kLineData.highPrice=row[5]
                kLineData.lowPrice=row[6]
                kLineData.closePrice=row[7]
                kLineData.volume=row[8]
                
                if lastDate!=row[2]:
                    #日切发送切换，持仓结算一次
                    self.SettleProfit("持仓结算")
                lastDate=row[2]
                
                if len(self.kLineDatas)>0 and kLineData.tms==self.kLineDatas[-1].tms :
                    #与KLine中上一个数据重复，则过滤
                    continue
                
                now=datetime.now()
                self.Algorithm(kLineData)
                cost=datetime.now()-now
                cost
            
        except(Exception) as ex:
            print("装载失败",ex)  
            logging.exception(ex)               
        #f.close()
        #处理完所有记录后再进行一次结算
        self.SettleProfit("持仓结算") 
                
             
     
        
    def CloseOrder(self):
        '''
                    平仓
        '''
        self.SettleProfit("平仓结算")       
        self.order=None
        
    def OpenOrder(self,direction,openTime,openPrice):
        '''
                    开仓
        '''
        self.order=Order(self.Instrument,direction,openTime,openPrice)
        
    def SettleProfit(self,type):
        if self.order==None:
            return
        newPrice=self.kLineDatas[-1].closePrice
        profit=(newPrice-self.order.LastSettlePrice)*int(self.TargetVolume)
        if self.order.Direction=="Short":
            profit=0-profit
        amt=profit*Strategy.Utils.GetMultiple(self.Instrument) 

        data=(self.kLineDatas[-1].tms.strftime('%Y%m%d %H:%M:%S'),type,self.__class__.__name__,
              self.Instrument,self.IntervalType,0,self.kLineDatas[-1].tms.strftime('%Y%m%d'),self.order.Direction,int(self.TargetVolume),str(self.order.IsTodayPosition),
              self.order.OpenTime.strftime('%Y%m%d %H:%M:%S'),self.order.OpenPrice,self.order.LastSettlePrice, self.kLineDatas[-1].closePrice,profit,amt,datetime.now())
        self.ProfitList.append(data)
        #self.sqliteConn.execute("INSERT INTO PROFIT VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",data)
        #self.sqliteConn.commit()
        
        self.order.IsTodayPosition=False
        self.order.LastSettlePrice=newPrice
        pass
    
        
        
class Order(object):
    '''
    classdocs
    '''
    Instrument=""
    Direction=""
    OpenTime=None
    OpenPrice=0
    IsTodayPosition=True
    LastSettlePrice=0

    def __init__(self,instrument,direction,openTime,openPrice):
        '''
        Constructor
        '''
        self.Direction=direction 
        self.OpenTime=openTime
        self.Instrument=instrument
        priceTick=Strategy.Utils.GetPriceTick(instrument)
        if self.Direction=="Short":
            priceTick=0-priceTick
        self.OpenPrice=openPrice+priceTick
        self.LastSettlePrice=self.OpenPrice 