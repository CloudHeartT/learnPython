# -*- coding = utf-8 -*-

import  requests
import urllib.request
import  urllib.response
from bs4 import BeautifulSoup
import re
import  os
import sys
import time
import datetime


#邮箱相关
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr,formataddr
from email.header import Header
from email.utils import formataddr,formatdate
import smtplib

# 以下两句代码在python 2 版本最好加上 避免编码错误
#reload(sys)
#sys.setdefaultencoding('utf-8')

class getContent():
    def __init__(self,questId):
    # 给出的第一个参数 就是你要下载的问题的id
    # 比如 想要下载的问题链接是 https://www.zhihu.com/question/29372574
    # 那么 就输入 python zhihu.py 29372574
        idHome = "/question/"+questId
        self.getAnswer(idHome)

    def save2file(self,fileName,content):
        fileName = fileName +".txt"
        f = open(fileName,'a',encoding='utf-8')
        f.write(content)
        f.close()

    def getAnswer(self,answerId):
        host = "http://www.zhihu.com"
        url = host + answerId
        print(url)
        userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/53.0.2785.116 Safari/537.36"
        #构造Header伪装浏览器
        Header = {"User-Agent" : userAgent}
        #请求该地址
        req = urllib.request.Request(url,headers=Header)
        #得到响应的内容
        try:
            response = urllib.request.urlopen(req , timeout= 20 )
            content = response.read()
            if content is None:
                print("Empty")
                return False
        except:
            print("timeOut,please try again")
            time.sleep(30)
            #try to switch proxy ip
            response = urllib.request.urlopen(req , timeout= 20)
            content = response.read()
            if content is None:
                print("Empty")
                return False

#此时已获取页面的完整代码，接着用BeautifulSoups比正则方便
        try:
            bs = BeautifulSoup(content,"lxml")
        except:
            print("BeautifulSoups Error")
            return False
        #获取该问题的标题
        title = bs.title
        if title is None:
            print("title is Empty")
            return False
        if title.string is None:
            print("string is Empty")
            return False
        fileName_old = title.string.strip()
        # 用来保存内容的文件名，因为文件名不能有一些特殊符号，所以使用正则表达式过滤掉
        fileName= re.sub('[\/:*?"<>|]', '-', fileName_old)
        self.save2file(fileName,title.string) #??????? 为什么此处的content是title.string 而不是 bs ????????????
        # 获取问题的补充内容
        detail = bs.find("div",class_ ="zm-editable-content") #class_ 是BeautifulSoup 的语法
        self.save2file(fileName, "\n\n\n\n--------------------Link %s ----------------------\n\n" % url)
        self.save2file(fileName, "\n\n\n\n--------------------Detail----------------------\n\n")
        if detail is not None:
            for i in detail.strings:
                self.save2file(fileName,i)

        #获取问题的回答

        answers = bs.find_all("div",class_="zm-editable-content clearfix")
        #定义参数
        k = 0
        index = 0
        for each_answer in answers:
            self.save2file(fileName, "\n\n-------------------------answer %s via  -------------------------\n\n" % k)
            #循环获取每一个答案的内容
            for a in each_answer.strings:
                self.save2file(fileName,a)
            k += 1
            index += 1

##################################################################
    #初始化邮箱相关参数
        smtp_server = 'smtp.126.com'
        from_mail = 'kindlezita@163.com'
        password = 'qqz123123'
        to_mail = '465731912@kindle','taotingme@163.com'

        #调用发送邮件的函数
        send_kindle=MailAbout(smtp_server,from_mail,password,to_mail)
        send_kindle.mail_text(fileName)
        print(fileName)
        # 调用发送邮件函数，把电子书发送到你的kindle用户的邮箱账号，这样你的kindle就可以收到电子书啦



class MailAbout():
    def __init__(self,stmp_server, from_mail, password, to_mail):
        self.server = stmp_server
        self.from_mail = from_mail
        self.password = password
        self.to_mail = to_mail
        self.subject = "我的知乎关注问题"+ datetime.datetime.now().strftime('%Y-%m-%d')

    #我们编写了一个函数_format_addr()来格式化一个邮件地址。注意不能简单地传入name <addr@example.com>，因为如果包含中文，需要通过Header对象进行编码。
    #msg['To']接收的是字符串而不是list，如果有多个邮件地址，用,分隔即可。
    #以下的三行format代码也可直接使用email.util里的formataddr
    # def __format__addr(self, format_spec):
    #     name, addr = parseaddr(format_spec)
    #     return formataddr((Header(name,'utf-8'), addr))

    def mail_text(self,fileName):

        #发送带附件的邮件时类型为MINEMutipart ,若不包含附件 直接使用MINEText即可
        #以下为设置邮件内容
        self.msg = MIMEMultipart()
        self.msg['From'] = formataddr('云心<%s>'% self.from_mail)
        self.msg['To'] = formataddr('myKindle<%s>'%self.to_mail)
        self.msg['Subject'] = Header(self.subject, 'utf-8').encode()
        self.msg['date'] =formatdate(localtime=1)
        self.fileName = fileName + ".txt"
        content = open(self.fileName.decode('utf-8'),'rb').read()
        print("**********************************邮件的内容##开始*******************************************")
        print(content)
        print("**********************************邮件的内容##结束*******************************************")
        #将得到的内容放入邮件附件
        self.att = MIMEText(content,'base64','utf-8')
        self.att['Content-Type'] = 'application/octet-stream'
        # self.att["Content-Disposition"] = "attachment;filename=\"%s\"" %(self.filename.encode('gb2312'))
        self.att["Content-Disposition"] = "attachment;filename=\"%s\"" % Header(self.fileName, 'gb2312')
        # print self.att["Content-Disposition"]

        #设置邮件的发送
        self.smtp = smtplib.SMTP()
        self.smtp.connect(self.server)
        self.smtp.login(self.from_mail,self.password)

        self.msg.attach(self.att)
        self.smtp.send_message(self.msg,self.msg['From'],self.msg['To'],self.msg.as_string())
        self.smtp.quit()


if __name__ == "__main__":
    #用于专门存放电子书的路径
    sub_folder = os.path.join(os.getcwd(),"content")

    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)

    os.chdir(sub_folder)

    #id = sys.argv[1] #这句代码体会一下， id也可以通过键盘输入得到
    #id = input("请输入需要转换为电子书的问题编码：")
    id = "20357585"
    # 给出的第一个参数 就是你要下载的问题的id
    # 比如 想要下载的问题链接是 https://www.zhihu.com/question/29372574
    # 那么 就输入 python zhihu.py 29372574


    # id_link="/question/"+id
    obj = getContent(id)

    print("程序运行完毕，该问题已导出为电子书！")