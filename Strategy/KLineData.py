'''
Created on 2016年8月24日

@author: duanqing
'''


class KLineData(object):
    '''
    classdocs
    '''
    tms=None
    instrumentId=""
    type=""
    offset=0
    openPrice=0
    highPrice=0
    lowPrice=0
    closePrice=0
    volume=0
    postion=0

    def __init__(self):
        '''
        Constructor
        '''
    
    def test(self):
        pass

    def __str__(self):
        return "[{0}-{1}-{2} {3} {4} {5}]".format(self.instrumentId,self.type,self.offset,self.tms,self.closePrice,self.volume)   