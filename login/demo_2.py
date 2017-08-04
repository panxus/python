#coding=utf-8
import requests
from bs4 import BeautifulSoup
import cookielib

class csTest(object):
    def __init__(self,headers):
        self.session = requests.Session()
        self.headers=headers
        cookie_filename = 'cookie.txt'
        self.session.cookies = cookielib.LWPCookieJar(cookie_filename)
        try:
            self.session.cookies.load(ignore_expires=True,ignore_discard=True)
        except:
            print("加载cookie失败,尝试重新登录")
            self.login_()
        else:
            print '加载cookie成功'
            # 加载cookie 成功 访问首页
            self.personWeb()

    def personWeb(self):
        print self.session.get('http://my.csdn.net/',headers=self.headers).content

    def login_(self):

        lt,execution = self.getData()
        form_data = {
            'username':'1058149613@qq.com',
            'password':'*****',
            'lt':lt,
            'execution':execution,
            '_eventId':'submit',
        }
        rs = self.session.post('https://passport.csdn.net/account/login',data=form_data,headers=self.headers)
        if rs.status_code == 200:
            print '登录成功'
            self.session.cookies.save(ignore_expires=True,ignore_discard=True)
        else:
            print '登录失败'
            print rs.content
    def getData(self):
        url = 'https://passport.csdn.net/account/login'
        con = self.session.get(url=url,headers=self.headers).content
        soup = BeautifulSoup(con,'lxml')
        lt = soup.find('input',{'name':'lt'})['value']
        execution = soup.find('input',{'name':'execution'})['value']
        return lt,execution

if __name__ == '__main__':
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    s = csTest(headers)
