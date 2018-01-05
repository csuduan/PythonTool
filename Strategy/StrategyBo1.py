'''
Created on 2016年8月29日

@author: duanqing
'''
from Strategy.BaseStrategy import BaseStrategy
import logging
import sys

class StrategyBo1(BaseStrategy):
    '''
    classdocs
    '''
    #参数
    LongN=0
    ShortN=0
    



        
    def Algorithm(self,kLinedata):
        self.kLineDatas.append(kLinedata)
        
        if len(self.kLineDatas)<self.LongN+1 :
            return
        
        logging.debug("{0}\t Bo1计算完成，时间:{1}  ".format(self.GetStrategyName(),kLinedata.tms))
        if self.order == None:
            maxHigh=0
            minLow=sys.float_info.max
            for i in range(1,self.LongN+1):
                maxHigh=max(self.kLineDatas[-1-i].highPrice,maxHigh)
                minLow=min(self.kLineDatas[-1-i].lowPrice,minLow)
            if kLinedata.closePrice >maxHigh:
                #开多
                self.OpenOrder("Long", kLinedata.tms,kLinedata.closePrice)
                logging.debug("{0}\t 准备开多  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return
            if kLinedata.closePrice<minLow:
                #开空
                self.OpenOrder("Short", kLinedata.tms,kLinedata.closePrice)
                logging.debug("{0}\t 准备开空  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return
        else:
            maxHigh=0
            minLow=sys.float_info.max
            for i in range(1,self.ShortN+1):
                maxHigh=max(self.kLineDatas[-1-i].highPrice,maxHigh)
                minLow=min(self.kLineDatas[-1-i].lowPrice,minLow)
            if self.order.Direction=="Long" and  kLinedata.closePrice < minLow:
                #平多
                self.CloseOrder()
                logging.debug("{0}\t准备平多[minLowPrice反转]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return
            if self.order.Direction=="Short" and kLinedata.closePrice>maxHigh:
                #开空
                self.CloseOrder()
                logging.debug("{0}\t准备平空[maxHighPrice反转]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return
                 
                
              