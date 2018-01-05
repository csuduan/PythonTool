'''
Created on 2016年8月29日

@author: duanqing
'''
from Strategy.BaseStrategy import BaseStrategy
import datetime
import logging

class StrategyTrend2(BaseStrategy):
    '''
    classdocs
    '''
    #参数
    LongKLineNum=0
    ShortKLineNum=0
    StopPercent=0.0
    IsBackClose=False
    
    #变量
    MaxPriceFromIn=0
    MinPriceFromIn=0
    
    CCI1=0
    CCI2=0
    


        
    def Algorithm(self,kLinedata):
        
        
        filerTime=datetime.datetime.strptime("09:00:00",'%H:%M:%S')
        if kLinedata.tms.time()==filerTime.time():
            return
        self.kLineDatas.append(kLinedata)
        
        
        
        if len(self.kLineDatas)<=self.LongKLineNum :
            return
        
        
        
        cci1=self.GetCCI(self.LongKLineNum)
        cci2=self.GetCCI(self.ShortKLineNum) 
        
        logging.debug("{0}\t Trend2计算完成，时间:{1}  cci1:{2} cci2:{3} CCI1:{4} CCI2:{5}".format(self.GetStrategyName(),kLinedata.tms,
                                        round(cci1,4),round(cci2,4),round(self.CCI1,4),round(self.CCI2,4)))   
        #CCI1初始状态        
        if self.CCI1==0:
            if cci1>100:
                self.CCI1=1
            elif cci1<-100:
                self.CCI1=-1
            else:
                return
            
        #CCI1反转,重置CCI2并平仓
        if self.CCI1==-1 and cci1>100:
            self.CCI1=1
            self.CCI2=0
            if self.order!=None:
                self.CloseOrder()
                logging.debug("{0}\t准备平仓[CCI1信号反转]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return
            
        if self.CCI1==1 and cci1<-100:
            self.CCI1=-1
            self.CCI2=0
            
            if self.order!=None:
                self.CloseOrder()
                logging.debug("{0}\t准备平仓[CCI1信号反转]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms)) 
                return  
        
        if self.CCI1==1:
            if self.order==None:
                #第一次从-100以下上穿到0
                if cci2<-100:
                    self.CCI2=-1
                if self.CCI2==-1 and cci2>0:
                    #开多
                    self.OpenOrder("Long", kLinedata.tms,kLinedata.closePrice)
                    logging.debug("{0}\t 准备开多  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                    self.MaxPriceFromIn=kLinedata.closePrice
                    return
            else:
                #cci2回踩-100则直接平仓，且不重置CCI2
                if self.IsBackClose==True and cci2 <-100:
                    self.CCI2=0
                    self.CloseOrder()
                    logging.debug("{0}\t准备平仓[cci2回踩]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                    return
        
        if self.CCI1==-1:
            if self.order==None:
                #第一次从 -100以下下穿到0
                if cci2>100:
                    self.CCI2=1
                if self.CCI2==1 and cci2<0:
                    #开空
                    self.OpenOrder("Short", kLinedata.tms,kLinedata.closePrice)
                    logging.debug("{0}\t 准备开空  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                    self.MinPriceFromIn=kLinedata.closePrice
                    return
            else:
                #cci2回踩100则直接平仓，且不重置CCI2
                if self.IsBackClose==True and cci2 >100:
                    self.CCI2=0
                    self.CloseOrder()
                    logging.debug("{0}\t准备平仓[cci2回踩]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                    return
        #移动止损
        if self.order!=None and self.order.Direction=="Long":
            self.MaxPriceFromIn=max(kLinedata.closePrice,self.MaxPriceFromIn)
            stopPrice=self.MaxPriceFromIn*(1-self.StopPercent)
            if kLinedata.closePrice<stopPrice:
                self.CCI2=0
                self.CloseOrder()
                logging.debug("{0}\t准备平仓[满足止损条件]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return
            
        if self.order!=None and self.order.Direction=="Short":
            self.MinPriceFromIn=min(kLinedata.closePrice,self.MinPriceFromIn)
            stopPrice=self.MinPriceFromIn*(1+self.StopPercent)
            if kLinedata.closePrice>stopPrice:
                self.CCI2=0
                self.CloseOrder()
                logging.debug("{0}\t准备平仓[满足止损条件]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return
            
    
    def GetCCI(self,k):     
        index=len(self.kLineDatas)
        sum=0
        for i in range(0,k):
            index-=1
            sum+=self.kLineDatas[index].closePrice
        avg=sum/k
        
        index=len(self.kLineDatas)
        sumDiff=0
        for i in range(0,k):
            index-=1
            sumDiff+=abs(self.kLineDatas[index].closePrice-avg)*0.015/k
            
        curMid=(self.kLineDatas[-1].highPrice+self.kLineDatas[-1].lowPrice+self.kLineDatas[-1].closePrice)/3
        if sumDiff==0:
            cci=0
        else:
            cci=(curMid-avg)/sumDiff
        return cci
        
        
