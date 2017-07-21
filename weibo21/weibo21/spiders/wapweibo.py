# -*- coding: utf-8 -*-
import scrapy
import re
import os
from urllib import urlretrieve

class WapweiboSpider(scrapy.Spider):
    name = 'wapweibo'
    folder = '张雪迎'
    uid = '1319911982'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    def start_requests(self):
        url = 'https://weibo.cn/u/'+self.uid
        yield scrapy.Request(url=url,headers=self.headers,meta={'cookiejar':1})
    def parse(self, response):
        imgs =  response.xpath('//img[contains(@src,"jpg")]/parent::a[contains(@href,"https")]')
        for img in imgs:
            new_link = img.xpath('@href').extract()[0]
            yield scrapy.Request(url=new_link,callback=self.getImage,headers=self.headers,meta={'cookiejar':response.meta['cookiejar']})
    def getImage(self,response):
        src = response.xpath('//img').extract()[0]
        print src
        # self.downImage(src,self.folder)
        # yield response.url
    def downImage(self,url,name):
        def get_name(path,url):
            return os.path.join(path,os.path.split(url)[1])
        if not os.path.isdir(name):
            os.mkdir(name)
        urlretrieve(url,get_name(name,url))