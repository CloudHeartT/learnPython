# -*- coding=utf-8 -*-

import requests
from http.cookiejar import LWPCookieJar
import re
import json
import time
import os
from getZhiHuContent import getContent

agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
Headers={'Host': 'www.zhihu.com',
         'Referer':'https://www/zhihu.com',
         'User-Agent':agent}

session = requests.session()
session.cookies = LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie can't load")

#判断是否登录成功
def isLogin():
    url = 'https://www.zhihu.com/settings/profile'
    return_code = session.get(url,headers = Headers, allow_redirects = False).status_code
    if return_code == 200:
        return True
        print("登录成功！")
    else:
        print("登录失败！")
        return False

