# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import os
from urllib import urlretrieve
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
class Wapweibo2Spider(scrapy.Spider):
    name = 'wapweibo2'

    user_name = raw_input('请输入用户名:\n')
    password = raw_input('请输入密码:\n')
    p_url = raw_input('输入wap版明星首页(例:https://weibo.cn/u/1223178222 空格回车):\n')
    folder = raw_input('输入文件夹名称:\n')
    # folder = fo.encode('gbk')

    start_urls = ['https://passport.weibo.cn/sso/login']
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    old_headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Host':'passport.weibo.cn',
        'Origin':'https://passport.weibo.cn',
        'Referer':'https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
    }
    def start_requests(self):
        url = 'https://passport.weibo.cn/sso/login'
        yield scrapy.Request(url=url,headers=self.old_headers,meta={'cookiejar':1})
    def parse(self, response):
        data = {
            'username':str(self.user_name).strip(),
            'password':str(self.password).strip(),
            'savestate':'1',
            'r':'http://weibo.cn/',
            'ec':'0',
            'pagerefer':'',
            'entry':'mweibo',
            'wentry':'',
            'loginfrom':'',
            'client_id':'','code':'','qq':'','mainpageflag':'1','hff':'','hfp':'',
        }
        yield FormRequest(url='https://passport.weibo.cn/sso/login',meta = {'cookiejar' : response.meta['cookiejar']},formdata = data,callback = self.after_login,headers=self.headers)

    def after_login(self,response):
        url = str(self.p_url).strip()
        yield scrapy.Request(url=url,meta={'cookiejar' : response.meta['cookiejar']},headers=self.headers,callback=self.downs)
    def downs(self,response):
        imgs =  response.xpath('//img[contains(@src,"jpg")]/parent::a[contains(@href,"https")]')
        for img in imgs:
            new_link = img.xpath('@href').extract()[0]
            yield scrapy.Request(url=new_link,callback=self.getImage,headers=self.headers,meta={'cookiejar':response.meta['cookiejar']})

    def getImage(self,response):
        src = response.xpath('//img/@src').extract()[0]
        self.downImage(src,self.folder)
        print src
    def downImage(self,url,name):
        def get_name(path,url):
            return os.path.join(path,os.path.split(url)[1])
        if not os.path.isdir(name):
            os.mkdir(name)
        urlretrieve(url,get_name(name,url))