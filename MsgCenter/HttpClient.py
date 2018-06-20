#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: duanqing
# @created on: 2018/6/7 10:37
# @desc  :

import urllib3
import json




def httpGet():
    url = 'http://192.168.1.11:5000/test'
    http = urllib3.PoolManager()
    resp = http.request('GET', url)
    print(resp.data)

def httpPost():
    url = 'http://192.168.1.11:5000/send'
    data = {"topic":"topic3","msg":"test from wxpy"}
    data=json.dumps(data).encode('utf-8')
    headers={"Content-Type":"application/json"}

    http = urllib3.PoolManager()
    resp = http.request('POST', url,body=data,headers=headers)
    print(resp.data)


if __name__ == "__main__":
    httpPost()


