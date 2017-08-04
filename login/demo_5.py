#coding=utf-8
import requests
from scrapy.selector import Selector
import cookielib
import time
from bs4 import BeautifulSoup
from urllib import urlretrieve
import os
class zhTest(object):
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        file = 'zh_cookie.txt'
        self.session = requests.Session()
        self.session.cookies = cookielib.LWPCookieJar(file)
        try:
            self.session.cookies.load(ignore_discard=True, ignore_expires=True)
        except:
            #faile reload login
            self.login_()
            pass
        else:
            pass
            self.myHome()

        pass

    def myHome(self):
        sc = self.session.get('https://www.zhihu.com/settings/profile',headers=self.headers)
        print sc.content


    def login_(self):
        _xsrf = self.getXsrf()
        login_url = 'https://www.zhihu.com/login/phone_num'
        login_data = {
            '_xsrf':_xsrf,
            'password':'*****',
            'captcha_type':'cn',
            'phone_num':'17607188711'
        }
        s = self.session.post(login_url,data=login_data,headers=self.headers)
        print s.text
        if s.status_code == 200:
            print '响应成功'
            # print s.text
            # print type(s.text)
            # print type(s.text['r'])
            con = eval(s.text)
            if int(con['r']) == 1:
                time_str = str(int(time.time()) * 1000)
                cap_url = 'https://www.zhihu.com/captcha.gif?r='+time_str+'&type=login'
                # urlretrieve(cap_url,'zh_code.gif')
                captcharesponse = self.session.get(cap_url,headers=self.headers)
                with open('checkcode.gif', 'wb') as f:
                    f.write(captcharesponse.content)
                    f.close()
                os.startfile('checkcode.gif')
                code = raw_input('code is:\n')
                login_data['captcha'] = code
                rs = self.session.post(login_url,data=login_data,headers=self.headers)
                print rs.text
                self.session.cookies.save(ignore_discard=True, ignore_expires=True)
                self.myHome()
            else:
                print s.text
        else:
            print '响应失败'

    def getXsrf(self):
        start_url = 'https://www.zhihu.com/'
        zHtml = self.session.get(start_url,headers=self.headers)
        indexSoup = BeautifulSoup(zHtml.content,'lxml')
        xsrf = indexSoup.find('input',{'name':'_xsrf'}).get('value')
        return xsrf






if __name__ == '__main__':
    oc = zhTest()


