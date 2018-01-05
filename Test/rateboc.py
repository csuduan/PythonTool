#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 17:48:43 2017

@author: Yunyun
"""

import urllib
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    __tempstr=str()
    __istd = False
    __inbody = False
    list = list()
    lasttime= str()
    def initlist(self):
        self.list = list()
        
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.__tempstr='' 
        elif tag == 'td':
            self.__istd = True
        elif tag == 'div':
            for k, v in attrs:
                if k == 'class' and v == 'BOC_main publish':
                    self.__inbody = True

    def handle_endtag(self, tag):
        if tag =='tr':
            if (self.__tempstr != ''):
                self.lasttime = self.__tempstr
                self.list.append(self.__tempstr)
            #print(self.laststr)
        elif tag == 'td':
            self.__istd = False
        elif tag == 'div':
            self.__inbody = False

    def handle_data(self, data):
            if self.__inbody == True:
                if self.__istd == True:
                    if(data.isspace()==False):  
                        self.__tempstr+=data+','
                                

parser = MyHTMLParser()
#定义一个要提交的数据数组(字典)
data = {}
#change input
data['erectDate'] = '2016-10-03'
data['nothing'] = '2017-10-04'
data['pjname'] = '1316'

#定义post的地址
url = 'http://srh.bankofchina.com/search/whpj/search.jsp'

start = 1
lastbench = ''
total = 0

while True:
    data['page'] = start

    post_data = urllib.parse.urlencode(data).encode('utf-8')
    #提交，发送数据
    req = urllib.request.urlopen(url, post_data)
     
    #获取提交后返回的信息
    content = req.read().decode('utf-8')
    parser.initlist()
    parser.feed(content)
    result = parser.lasttime.split(',')
    if lastbench == '':
        lastbench = result[7]
    elif lastbench == result[7]:
        break
    else:
        lastbench = result[7]
    total+=len(parser.list)
    for value in parser.list:  
        print(value) 
    start = start + 1
        
print('get pages:' + str(start-1)+", and size:" + str(total))
#for value in liststr:  
 #   print(value)  
