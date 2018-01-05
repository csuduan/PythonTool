#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib
import urllib.parse
import base64
import time
#----------------------------------
# 验证码识别调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/60
#----------------------------------

def main():

    #配置您申请的APPKey
    appkey = "e1f7d3a42368f034db29506383f09d82"

    #1.识别验证码
    now=time.time()
    request1(appkey,"GET")
    print(time.time()-now)

    #2.查询验证码类型代码
    #request2(appkey,"GET")



#识别验证码
def request1(appkey, m="GET"):
    url = "http://op.juhe.cn/vercode/index"
    image=open(r'111.jpg','rb')
    base=base64.b64encode(image.read())
    image.close()
    params = {
        "key" : appkey, #您申请到的APPKEY
        "codeType" : "1006", #验证码的类型，&lt;a href=&quot;http://www.juhe.cn/docs/api/id/60/aid/352&quot; target=&quot;_blank&quot;&gt;查询&lt;/a&gt;
        "image" : "111.jpg", #图片文件
        "base64Str":base,
        "dtype" : "json", #返回的数据的格式，json或xml，默认为json

    }
    params = urllib.parse.urlencode(params)
    if m =="GET":
        f = urllib.request.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.request.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"],res["reason"]))
    else:
        print("request api error")



if __name__ == '__main__':
    main()