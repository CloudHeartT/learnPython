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

    #登录时获取验证码
def get_Captcha():
    #r = 1487059817671
    r= time.time()*1000
    url = 'https://www.zhihu.com/captcha.gif?r='+str(r)+'&type=login'
    #知乎现在的验证码有两种形式，一种是普通的填写四个字母，还有一种是点击倒立的汉字
        #第二种需要在type后追加参数 如https://www.zhihu.com/captcha.gif?r="+str(r)+"&type=login&lang=cn
    image = session.get(url,headers = Headers)
    f = open("photo.jpg",'wb')
    f.write(f.content)
    f.close()

def Login():
    #取到xsrf
    xsrf = get_xsrf()
    url = "https://www.zhihu.com/login/email"
    data = {
        'xsrf' :xsrf,
        'email' : '465731912@qq.com',
        'password' : 'qqz123123',
        'remember_me':'true'
    }
    try:
        login_content = session.post(url, data, headers=Headers)
        text = login_content.text
        status_code = login_content.status_code
        print("登录的状态码为："+ status_code)
        #判断状态码
        if status_code != requests.codes.ok:
            print("自动登录失败，需要输入验证码")
            get_Captcha()
            code = input("请输入看到的验证码内容")
            data['captcha'] = code
            login_content = session.post(url,data,headers = Headers)
            status_code = login_content.status_code
            if status_code == requests.code.ok:
                print("登陆成功（已输验证码）")
                session.cookies.save()
        else:

            print("登录成功！")
            session.cookies.save()
    except:
        print("Error in Login")
        return False
