'''
Created on 2016年8月29日

@author: duanqing
'''
from Strategy.BaseStrategy import BaseStrategy
import Strategy.Utils
import datetime
import logging
import sys

class StrategyTrend3(BaseStrategy):
    '''
    classdocs
    '''
    #参数
    R=0.0
    T1=0
    T2=0

    #变量
    UpperLimit=sys.float_info.max
    LowLimit=sys.float_info.min
    
    MaxClosePrice=0
    MinClosePrice=0
    
    Direct=1


        
    def Algorithm(self,kLinedata):
            
        self.kLineDatas.append(kLinedata)
        if self.Direct==1:
            self.MaxClosePrice=max(kLinedata.closePrice,self.MaxClosePrice)
            if kLinedata.closePrice<=(1-self.R/100)*self.MaxClosePrice:
                self.UpperLimit=self.MaxClosePrice
                self.Direct=-1
                self.MinClosePrice=kLinedata.closePrice
                self.MaxClosePrice=sys.float_info.min
        
        if self.Direct==-1:
            self.MinClosePrice=min(kLinedata.closePrice,self.MinClosePrice)
            if kLinedata.closePrice>=(1+self.R/100)*self.MinClosePrice:
                self.LowLimit=self.MinClosePrice
                self.Direct=1
                self.MaxClosePrice=kLinedata.closePrice
                self.MinClosePrice=sys.float_info.max
        
        
        
        if len(self.kLineDatas)<52:
            return
        logging.debug("{0}\t Trend3计算完成，时间:{1}  方向:{2} 上界:{3} 下界:{4} T9:{5} T26:{6} T52:{7}".format(self.GetStrategyName(),kLinedata.tms,
                                        self.Direct,self.UpperLimit,self.LowLimit,self.GetAvgHL(9),self.GetAvgHL(26),self.GetAvgHL(52)))
        
        #if kLinedata.tms.strftime('%Y%m%d') =='20160506':
        #    a=1

        if self.order==None:
            if (self.GetAvgHL(9)+self.GetAvgHL(26))/2-self.GetAvgHL(52)>self.T1*Strategy.Utils.GetPriceTick(self.Instrument) \
            and kLinedata.closePrice > self.UpperLimit:
                self.OpenOrder("Long", kLinedata.tms,kLinedata.closePrice)
                logging.debug("{0}\t 准备开多  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return
            
            if self.GetAvgHL(52)-(self.GetAvgHL(9)+self.GetAvgHL(26))/2>self.T1*Strategy.Utils.GetPriceTick(self.Instrument)\
            and kLinedata.closePrice < self.LowLimit:
                self.OpenOrder("Short", kLinedata.tms,kLinedata.closePrice)
                logging.debug("{0}\t 准备开空  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return 
        else:

            if self.order.Direction=="Long" and self.GetAvgHL(9)-kLinedata.closePrice>self.T2*Strategy.Utils.GetPriceTick(self.Instrument) :
                self.CloseOrder()
                logging.debug("{0}\t准备平仓[满足平多]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return
            
            if self.order.Direction=="Short" and kLinedata.closePrice-self.GetAvgHL(9)>self.T2*Strategy.Utils.GetPriceTick(self.Instrument)\
            and kLinedata.closePrice < self.LowLimit:
                self.OpenOrder("Short", kLinedata.tms,kLinedata.closePrice)
                logging.debug("{0}\t准备平仓[满足平空]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return
            
            
    
    def GetAvgHL(self,t):
        maxHigh=0
        minLow=sys.float_info.max
        for i in range(1,t+1):
            if self.kLineDatas[-i].highPrice !=None:
                maxHigh=max(self.kLineDatas[-i].highPrice,maxHigh)
            if self.kLineDatas[-i].lowPrice !=None:
                minLow=min(self.kLineDatas[-i].lowPrice,minLow)
            
        return (maxHigh+minLow)/2
        
        
