#!/usr/bin/python3

import os
import time
import re
#import paramiko
import shutil


a=os.path.exists(r'C:\Users')


print("a")

import pycurl
import io

url='http://180.167.77.18:8090/pages/viewpage.action?pageId=3309635'
c=pycurl.Curl()
c.setopt(c.URL, url)

b = io.BytesIO()
c.setopt(c.WRITEDATA, b)
c.setopt(c.USERPWD, 'duanqing:715300')


#c.setopt(c.FOLLOWLOCATION, 1)
#c.setopt(c.HEADER, True)

c.perform()
body=b.getvalue()
print (body.decode('utf8'))

b.close()
c.close()