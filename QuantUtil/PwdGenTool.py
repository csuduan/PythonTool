#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 账户密码生成工具

#注意！！！   需要安装pydes模块 ：pip install pydes

from pyDes import *
import base64
from bs4 import BeautifulSoup
import pycurl
import io

key='12345678'
iv='20161123'
url='http://180.167.77.18:8090/pages/viewpage.action?pageId=3309635'
userpwd='test:test!!'

def DesEncrypt(str):
    k = des(key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    EncryptStr = k.encrypt(str)
    result=base64.b64encode(EncryptStr)
    return bytes.decode(result)

def main():
    results=[]
    # file=open('pwd.txt','r')
    # lines=file.readlines()
    #
    # for line in lines:
    #     encryptedPwd=DesEncrypt(line.rstrip('\n'))
    #     print(encryptedPwd)
    #     results.append(encryptedPwd+'\n')
    # file.close()


    accounts=getPwd()
    accounts.append("000303|123123")

    for account in accounts:
        encryptedPwd=DesEncrypt(account)
        print(encryptedPwd)
        results.append(encryptedPwd+'\n')

    fileRet=open('pwd.txt','w')
    fileRet.writelines(results)
    fileRet.close()

    pass

def getPwd():

    c=pycurl.Curl()
    c.setopt(c.URL, url)

    b = io.BytesIO()
    c.setopt(c.WRITEDATA, b)
    c.setopt(c.USERPWD, 'tradingassistant:tradingassistant!')

    #c.setopt(c.FOLLOWLOCATION, 1)
    #c.setopt(c.HEADER, True)

    c.perform()
    html=b.getvalue().decode('utf8')


    b.close()
    c.close()

    #解析html
    results=[]
    soup = BeautifulSoup(html, 'html.parser')
    trs=soup.find('tbody').findAll('tr')[1:]
    for tr in  trs:
        try:
            tds=tr.findAll('td')
            account=tds[4].text.replace(u'\xa0', u'')
            pwd=tds[5].text.replace(u'\xa0', u'')


            if account !='':
                results.append(account+'|'+pwd)
        except Exception as ex:
            print(ex)

    print(results)
    return results

if __name__ == '__main__':
    main()
