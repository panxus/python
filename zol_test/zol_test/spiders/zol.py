# -*- coding: utf-8 -*-
# 默认尺寸 960*600
import scrapy
from urllib import urlretrieve
from zol_test.items import ZolTestItem
import os

class ZolSpider(scrapy.Spider):
    name = 'zol'
    old_url = 'http://desk.zol.com.cn'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    def start_requests(self):
        url = 'http://desk.zol.com.cn/fengjing/'
        yield scrapy.Request(url,headers=self.headers)

    def parse(self, response):
        lis = response.xpath('//li[@class="photo-list-padding"]')
        for li in lis:
            item = ZolTestItem()
            item['name'] = li.xpath('a/span/em/text()').extract()[0].strip()
            url = li.xpath('a/@href').extract()[0]
            yield scrapy.Request(url=self.old_url + url,meta={'item':item,'name':item['name']},callback=self.real_url,headers=self.headers)

    def real_url(self,response):
        item = response.meta['item']
        liBox = response.xpath('//*[@id="showImg"]/li')
        for ili in liBox:
            href = ili.xpath('a/@href').extract()[0]
            yield scrapy.Request(url=self.old_url+href,meta={'item':item,'name':item['name']},callback=self.last_url,headers=self.headers)

    def last_url(self,response):
        name = response.meta['name']
        item = response.meta['item']
        img_url = response.xpath('//*[@id="bigImg"]/@src').extract()[0]
        self.downImage(img_url,name)
        yield item

    def downImage(self,url,name):
        def get_name(path,url):
            return os.path.join(path,os.path.split(url)[1])
        if not os.path.isdir(name):
            os.mkdir(name)
        urlretrieve(url,get_name(name,url))