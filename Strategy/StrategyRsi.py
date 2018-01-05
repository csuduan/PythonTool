from Strategy.BaseStrategy import BaseStrategy

from datetime import datetime,timedelta  
import logging
'''
Created on 2016年8月24日

@author: duanqing
'''

class StrategyRsi(BaseStrategy):
    '''
    StrategyRsi
    '''
    #参数
    Min4mAvgVolumeChange=0.0
    Max4mAvgVolumeChange = 0.0
    InValidTimes= "09:00-09:06,13:30-13:36"
    NotHLPirceFromOpen = False
    NotHLPirceIn60m = False
    NotHLPirceFrom0930 = False
    Min10mPriceChange = 0.0
    Max30mPriceChange = 0.0
    CheckPre4AvgRsi = False
    CloseRsiOffset = 0.0
    StopPoint = 0.0
    
    #变量
    rsiDatas=[]
    UP_RSI=80
    DOWN_RSI=20
    CLOSE_RSI=50


    def RunCurrentInstrumentOnly(self):
        return True
    
    def GetHLPriceFromStarts(self,starTimes,kLineData):
        '''
                    从指定起点获取最大最小值
        '''
        max=self.kLineDatas[-1].closePrice
        min=self.kLineDatas[-1].closePrice         
        if len(self.kLineDatas)>1:
            startIndex=len(self.kLineDatas)-2
            while startIndex>=0 and self.kLineDatas[startIndex].tms.date()==kLineData.tms.date():
                for start in starTimes:
                    if self.kLineDatas[startIndex].tms.time() == start.time():
                        return max,min
                if self.kLineDatas[startIndex].closePrice>max:
                    max=self.kLineDatas[startIndex].closePrice
                if self.kLineDatas[startIndex].closePrice<min:
                    min=self.kLineDatas[startIndex].closePrice
                startIndex-=1
            pass
        return max,min
                
    def GetBeforeMaxAndMinPrice(self,count):
        '''
                    查找前n个Tick最大值与最小值(跨天)
        '''
        maxPrice=self.kLineDatas[-1].closePrice
        minPrice=self.kLineDatas[-1].closePrice 
        
        startIndex=len(self.kLineDatas)-2
        while count>0 and startIndex>=0:
            
            maxPrice=max(self.kLineDatas[startIndex].closePrice,maxPrice)
            minPrice=min(self.kLineDatas[startIndex].closePrice,minPrice)
            startIndex-=1
            count-=1    
        return maxPrice,minPrice                                
                
    
    def CheckOpen(self,kLineData):
        '''
                    开仓条件检测
        '''
        openCheck=True
        
        #//检测是否在无效时间中
        for timePair in self.InValidTimes.split(','):
            start=datetime.strptime(timePair.split('-')[0],'%H:%M')
            end=datetime.strptime(timePair.split('-')[1],'%H:%M')
            if kLineData.tms.time() >=start.time() and kLineData.tms.time()<=end.time():
                logging
                return False
                
         #非开盘起最高最低价   
        if self.NotHLPirceFromOpen:
            startTiems=[]
            startTiems.append(self.tradeTime.DayOpenTime)
            startTiems.append(self.tradeTime.NightOpenTime)
            
            #非9:30起最高最低价,则将9:30加入到起点
            if self.NotHLPirceFrom0930:
                startTiems.append(datetime.strptime("09:30:00",'%H:%M:%S'))
            
            (max,min)=self.GetHLPriceFromStarts(startTiems,kLineData)
            if kLineData.closePrice == max or kLineData.closePrice == min:
                return False
            
        
        # 非1h内最高最低价   
        if  self.NotHLPirceIn60m :
            max,min=self.GetBeforeMaxAndMinPrice(59)
            if kLineData.closePrice == max or kLineData.closePrice == min:
                return False
        
        #前4分钟平均成交量的变化
        if self.Min4mAvgVolumeChange!=0 or self.Max4mAvgVolumeChange!=0:
            list=self.kLineDatas[-5:-1]
            sum=0
            for x in list:
                if x.tms.date()!=kLineData.tms.date():
                    return False
                sum+=x.volume
            avgVold=sum/4
            curVold=kLineData.volume
            
            Min4mAvgVolumeChange=float(self.Min4mAvgVolumeChange)
            if Min4mAvgVolumeChange!=0:
                if curVold <= Min4mAvgVolumeChange*avgVold:
                    return False
            if self.Max4mAvgVolumeChange!=0:
                if curVold>=float(self.Max4mAvgVolumeChange)*avgVold:
                    return False
         
        #10分钟价格波动最小千分比
        Min10mPriceChange=float(self.Min10mPriceChange)/1000
        if self.Min10mPriceChange !=0:
            max,min=self.GetBeforeMaxAndMinPrice(59)
            if (max-min)<=Min10mPriceChange*kLineData.closePrice:
                return False
        
        #30分钟价格波动最小千分比
        Max30mPriceChange=float(self.Max30mPriceChange)/1000
        if Max30mPriceChange!=0:
            max,min=self.GetBeforeMaxAndMinPrice(59)
            if (max-min)>=  Max30mPriceChange*kLineData.closePrice:
                return False
               
        return True    
                                    
    
    def GetRecentAvgRsi(self,count):
        '''
                    获取最近平均RSI
        '''
        if count>len( self.rsiDatas):
            count=len( self.rsiDatas)
        
        startIndex=len( self.rsiDatas)-1
        sum=0
        num=count
        
        while num>0:
            sum+=self.rsiDatas[startIndex].rsi
            startIndex-=1
            num-=1
        return sum/count
    
    def Algorithm(self,kLinedata):
        now=datetime.now()
        rsiData=RsiData()
        rsiData.tms=kLinedata.tms
        rsiData.closePrice=kLinedata.closePrice
        
        self.rsiDatas.append(rsiData)
        self.kLineDatas.append(kLinedata)
        
        self.Rsi()
        #cost=datetime.now()-now
        #now=datetime.now()
        lastRsiData=self.rsiDatas[-1]
        rsi=lastRsiData.rsi
        logging.debug("{0}\t Rsi计算完成，时间:{1}  值:{2}".format(self.GetStrategyName(),kLinedata.tms,rsi))
        
        
        
        if rsi==0:
            return
        
        
        time=kLinedata.tms.time()
        
        
        #开盘前7分钟不做分析
        if time>=self.tradeTime.DayOpenTime.time() and time<=(self.tradeTime.DayOpenTime+timedelta(seconds=60*7)).time() :
            return
        if time>=self.tradeTime.NightOpenTime.time() and time<=(self.tradeTime.NightOpenTime+timedelta(seconds=60*7)).time() :
            return
        
        #收盘处理
        if time<=self.tradeTime.DayCloseTime.time() and time>=(self.tradeTime.DayCloseTime-timedelta(seconds=60*3)).time() \
        or time<=self.tradeTime.NigthCloseTime.time() and time>=(self.tradeTime.NigthCloseTime-timedelta(seconds=60*3)).time():
            if self.order:
                self.CloseOrder()
                #print("{0}\t 收盘强平  时间:{1}",self.GetStrategyName(),kLinedata.tms)
                logging.debug("{0}\t 收盘强平  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
        
        #正式处理
        if self.order ==None:
            #开仓检测
            if rsi>=self.UP_RSI and self.CheckOpen(kLinedata):
                #开空
                self.OpenOrder("Short",kLinedata.tms,kLinedata.closePrice)
                #print("{0}\t 准备开空  时间:{1}",self.GetStrategyName(),kLinedata.tms)
                logging.debug("{0}\t 准备开空  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
            if rsi<=self.DOWN_RSI and self.CheckOpen(kLinedata):
                #开多
                self.OpenOrder("Long",kLinedata.tms,kLinedata.closePrice)
                #print("{0}\t 准备开多  时间:{1}",self.GetStrategyName(),kLinedata.tms)
                logging.debug("{0}\t 准备开多  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))    
        elif self.order.Direction=="Long":
            #平多检测
            if rsi > self.CLOSE_RSI+self.CloseRsiOffset:
                self.CloseOrder()
                #print("{0}\t准备平多[RSI值满足平仓条件]  时间:{1}",self.GetStrategyName(),kLinedata.tms) 
                logging.debug("{0}\t准备平多[RSI值满足平仓条件]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return 
            
            if self.CheckPre4AvgRsi and   self.GetRecentAvgRsi(5)<self.DOWN_RSI:
                self.CloseOrder()
                #print("{0}\t准备平多[连续4分钟RSI值满足平仓条件]  时间:{1}",self.GetStrategyName(),kLinedata.tms)
                logging.debug("{0}\t准备平多[连续4分钟RSI值满足平仓条件]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return
                       
            loss=self.order.OpenPrice- lastRsiData.closePrice 
            if self.StopPoint!=0 and loss>self.StopPoint:
                self.CloseOrder()
                #print("{0}\t准备平多[亏损点{1}满足平仓条件]  时间:{2}",self.GetStrategyName(),loss,kLinedata.tms)
                logging.debug("{0}\t准备平多[亏损点{1}满足平仓条件]  时间:{2}".format(self.GetStrategyName(),loss,kLinedata.tms))
                return
            #涨停检测
            #。。。                        
            
        else:
            #平空检测
            if rsi < self.CLOSE_RSI-self.CloseRsiOffset:
                self.CloseOrder()
                #print("{0}\t准备平空[RSI值满足平仓条件]  时间:{1}",self.GetStrategyName(),kLinedata.tms) 
                logging.debug("{0}\t准备平空[RSI值满足平仓条件]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms)) 
                return
            
            if self.CheckPre4AvgRsi and   self.GetRecentAvgRsi(5)>self.UP_RSI:
                self.CloseOrder()
                #print("{0}\t准备平空[连续4分钟RSI值满足平仓条件]  时间:{1}",self.GetStrategyName(),kLinedata.tms)
                logging.debug("{0}\t准备平空[连续4分钟RSI值满足平仓条件]  时间:{1}".format(self.GetStrategyName(),kLinedata.tms))
                return
            
            loss=lastRsiData.closePrice -self.order.OpenPrice
            if self.StopPoint!=0 and loss>self.StopPoint:
                self.CloseOrder()
                #print("{0}\t准备平空[亏损点{1}满足平仓条件]  时间:{2}",self.GetStrategyName(),loss,kLinedata.tms)
                logging.debug("{0}\t准备平空[亏损点{1}满足平仓条件]  时间:{2}".format(self.GetStrategyName(),loss,kLinedata.tms))
                return
            
        cost=datetime.now()-now
        now=datetime.now()    
        
    def Rsi(self):
        index=len(self.rsiDatas)-1
        if index==0:
            self.rsiDatas[0].rsi=0
        elif index<=7:
            diff=self.rsiDatas[index].closePrice-self.rsiDatas[index-1].closePrice
            if diff>=0:
                self.rsiDatas[index].up=diff
            else:
                self.rsiDatas[index].down=-diff
            
            if(index==7):
                for x in self.rsiDatas:
                    self.rsiDatas[index].avgUp+=x.up/7
                    self.rsiDatas[index].avgDown+=x.down/7
                self.rsiDatas[index].rsi=self.rsiDatas[index].avgUp/(self.rsiDatas[index].avgUp+self.rsiDatas[index].avgDown)*100
        else:
            diff=  self.rsiDatas[index].closePrice-self.rsiDatas[index-1].closePrice
            if diff>=0:
                 self.rsiDatas[index].up=diff
                 self.rsiDatas[index].down=0
            else:
                self.rsiDatas[index].down=0-diff
                self.rsiDatas[index].up=0
            
            self.rsiDatas[index].avgUp=(self.rsiDatas[index-1].avgUp*6+self.rsiDatas[index].up)/7
            self.rsiDatas[index].avgDown=(self.rsiDatas[index-1].avgDown*6+self.rsiDatas[index].down)/7
            self.rsiDatas[index].rsi=self.rsiDatas[index].avgUp /(self.rsiDatas[index].avgUp+self.rsiDatas[index].avgDown)*100
            
            
        



'''
RsiData
'''        
class RsiData:
    tms=""
    rsi=0
    closePrice=0
    up=0;
    down=0;
    avgUp=0;
    avgDown=0;
    
    def __init__(self):
        '''
        Constructor
        '''