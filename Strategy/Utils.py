'''
Created on 2016年8月25日

@author: duanqing
'''

import re
from datetime import datetime,timedelta 

InstrumentInfo={}
InstrumentInfo['a']=(10,1)
InstrumentInfo['b']=(10,1)
InstrumentInfo['bb']=(500,0.05)
InstrumentInfo['c']=(10,1)
InstrumentInfo['cs']=(10,1)
InstrumentInfo['fb']=(500,0.05)
InstrumentInfo['i']=(100,0.5)
InstrumentInfo['j']=(100,0.5)
InstrumentInfo['jd']=(10,1)
InstrumentInfo['jm']=(60,0.5)
InstrumentInfo['l']=(5,5)
InstrumentInfo['m']=(10,1)
InstrumentInfo['p']=(10,2)
InstrumentInfo['pp']=(5,1)
InstrumentInfo['v']=(5,5)
InstrumentInfo['y']=(10,2)
InstrumentInfo['ag']=(15,1)
InstrumentInfo['al']=(5,5)
InstrumentInfo['au']=(1000,0.05)
InstrumentInfo['bu']=(10,2)
InstrumentInfo['cu']=(5,10)
InstrumentInfo['fu']=(50,1)
InstrumentInfo['hc']=(10,1)
InstrumentInfo['ni']=(1,10)
InstrumentInfo['pb']=(5,5)
InstrumentInfo['rb']=(10,1)
InstrumentInfo['ru']=(10,5)
InstrumentInfo['sn']=(1,10)
InstrumentInfo['wr']=(10,1)
InstrumentInfo['zn']=(5,5)
InstrumentInfo['CF']=(5,5)
InstrumentInfo['FG']=(20,1)
InstrumentInfo['JR']=(20,1)
InstrumentInfo['LR']=(20,1)
InstrumentInfo['MA']=(10,1)
InstrumentInfo['OI']=(10,2)
InstrumentInfo['PM']=(50,1)
InstrumentInfo['RI']=(20,1)
InstrumentInfo['RM']=(10,1)
InstrumentInfo['RS']=(10,1)
InstrumentInfo['SF']=(5,2)
InstrumentInfo['SM']=(5,2)
InstrumentInfo['SR']=(10,1)
InstrumentInfo['TA']=(5,2)
InstrumentInfo['WH']=(20,1)
InstrumentInfo['ZC']=(100,0.2)


class TradeTime(object):
    '''
    classdocs
    '''
    DayOpenTime=None
    DayCloseTime=None
    NightOpenTime=None
    NigthCloseTime=None

    def __init__(self,dayCloseTime,nightCloseTime,dayOpenTime="09:00:00",nightOpenTime="21:00:00"):
        '''
        Constructor
        '''
        self.DayCloseTime=datetime.strptime(dayCloseTime,'%H:%M:%S')
        self.DayOpenTime= datetime.strptime(dayOpenTime,'%H:%M:%S')
        self.NightOpenTime= datetime.strptime(nightOpenTime,'%H:%M:%S')
        self.NigthCloseTime= datetime.strptime(nightCloseTime,'%H:%M:%S')


def GetTradeTime(instrument):
    '''
        获取交易时间
    '''
    
    product=re.sub(r'\d',"",instrument)
    tradeTime=None
    if   product in ("ru","bu","rb","hc"):
        tradeTime=TradeTime("15:00:00", "23:00:00")
        return tradeTime
    elif   product in ("au","ag"):
        tradeTime=TradeTime("15:00:00", "02:30:00")
        return tradeTime
    elif product in ("cu","al","zn","pb","ni","sn","fu"):
        tradeTime=TradeTime("15:00:00", "01:00:00")
        return tradeTime
    elif product in ('TA','SR','MA','RM','FG','CF','OI','ZC','WH','SM','SF','RI','LR','RS','JR'):
        tradeTime=TradeTime("15:00:00", "23:30:00")
        return tradeTime  
    elif product in ('jd','p','m','y','a','c','cs','bb','fb','l','v','i','b','j','jm'):
        tradeTime=TradeTime("15:00:00", "23:30:00")
        return tradeTime
    else:
        tradeTime=TradeTime("15:00:00", "23:30:00")
        return tradeTime
    
    print("获取合约交易时间失败",instrument)  
    
def GetMultiple(instrument):
    '''
           获取合约乘数
    '''
    product=re.sub(r'\d',"",instrument)
    return InstrumentInfo[product][0] 

def GetPriceTick(instrument):
    '''
          获取点差
    '''
    product=re.sub(r'\d',"",instrument)
    return InstrumentInfo[product][1]        
             