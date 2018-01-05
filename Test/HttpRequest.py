# -*- coding: utf8 -*-
#!/usr/bin/python

import sys
import urllib.request as request
import json

print("aa")

response=request.urlopen("http://www.baidu.com");
html=response.read()
print(html)