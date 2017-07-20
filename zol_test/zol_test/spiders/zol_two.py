# -*- coding: utf-8 -*-
# 再次请求 大尺寸 1920x1080
import scrapy
from urllib import urlretrieve
from zol_test.items import ZolTestItem
import os

class ZolSpider(scrapy.Spider):
    name = 'zol_2'
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
            if response.url.split('cn')[-1] == href:
                #  避免scrapy过滤重复请求机制
                href = href + '?sss'
            # print href
            yield scrapy.Request(url=self.old_url+href,meta={'item':item,'name':item['name']},callback=self.last_url,headers=self.headers)

    def last_url(self,response):
        item = response.meta['item']
        img_links = response.xpath('//*[@id="1920x1080"]/@href').extract()
        if not img_links:
            img_links = response.xpath('//*[@id="1680x1050"]/@href').extract()
        img_link = img_links[0]

        if img_link:
            yield scrapy.Request(url=self.old_url+img_link,meta={'item':item,'name':item['name']},callback=self.find_url,headers=self.headers)
        yield item

    def find_url(self,response):
        name = response.meta['name']
        src = response.xpath('/html/body/img[1]/@src').extract()[0]
        self.downImage(src,name)

    def downImage(self,url,name):
        def get_name(path,url):
            return os.path.join(path,os.path.split(url)[1])
        if not os.path.isdir(name):
            os.mkdir(name)
        urlretrieve(url,get_name(name,url))