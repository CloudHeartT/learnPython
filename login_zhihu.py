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

#登陆成功后获取其中的_xsrf
def get_xsrf():
    url='http://www.zhihu.com'
    r=session.get(url,headers=headers,allow_redirects=False)
    txt=r.text
    result=re.findall(r'<input type=\"hidden\" name=\"_xsrf\" value=\"(\w+)\"/>',txt)[0]
    return result

def getCaptcha():
    #r=1471341285051
    r=(time.time()*1000)
    url='http://www.zhihu.com/captcha.gif?r='+str(r)+'&type=login'

    image=session.get(url,headers=headers)
    f=open("photo.jpg",'wb')
    f.write(image.content)
    f.close()
