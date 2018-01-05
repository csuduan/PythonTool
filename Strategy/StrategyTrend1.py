'''
Created on 2016年8月29日

@author: duanqing
'''
from Strategy.BaseStrategy import BaseStrategy
import logging
import sqlite3

class StrategyTrend1(BaseStrategy):
    '''
    classdocs
    '''
    #参数
    FastK=0
    SlowK=0
    DayN=0
    Threshold=0.0
    
    #变量
    LastFastEma=0
    LastSlowEma=0


        
    def Algorithm(self,kLinedata):
        self.kLineDatas.append(kLinedata)
        
        if len(self.kLineDatas)<=int(self.DayN) :
            return
        
        endIndex=len(self.kLineDatas)-1
        startIndex=endIndex-int(self.DayN)
        shift=self.kLineDatas[endIndex].closePrice-self.kLineDatas[startIndex].closePrice
        distance=0
        for i in range(startIndex+1,endIndex+1):
            distance+=abs(self.kLineDatas[i].closePrice-self.kLineDatas[i-1].closePrice)
            
        ratio=shift/distance
        fastEma= self.GetEma(self.FastK, self.LastFastEma, ratio) 
        showEma=self.GetEma(self.SlowK, self.LastSlowEma, ratio)
        
        logging.debug("{0}\t Trend1计算完成，时间:{1}  shift:{2} distance:{3} fastEma:{4} showEma:{5}".format(self.GetStrategyName(),kLinedata.tms,
                                                                                                       shift,distance,fastEma,showEma))
        if self.LastFastEma<self.LastFastEma+self.Threshold and fastEma>showEma + self.Threshold:
            if self.order==None or self.order.Direction!="Long":
                #Fast上穿Slow，且未开多，开多
                if self.order!=None and self.order.Direction=="Short":
                    self.CloseOrder()
                    logging.debug("{0}\t 准备反平  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                self.OpenOrder("Long", kLinedata.tms,kLinedata.closePrice)
                logging.debug("{0}\t 准备开多  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                self.LastFastEma=fastEma
                self.LastSlowEma=showEma
                
        if self.LastFastEma>self.LastFastEma-self.Threshold and fastEma<showEma - self.Threshold:
            if self.order==None or self.order.Direction!="Short":
                #Fast下穿Slow，且未开空，开空
                if self.order!=None and self.order.Direction=="Long":
                    self.CloseOrder()
                    logging.debug("{0}\t 准备反平  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                self.OpenOrder("Short", kLinedata.tms,kLinedata.closePrice)
                logging.debug("{0}\t 准备开空  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                self.LastFastEma=fastEma
                self.LastSlowEma=showEma 
        self.LastFastEma=fastEma
        self.LastSlowEma=showEma      
                
          
    def GetEma(self,k,lastEma,ratio):
        return lastEma*(k-1)/(k+1) +ratio*2/(k+1)        