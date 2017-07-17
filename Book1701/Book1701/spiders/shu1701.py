# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from Book1701.items import Book1701Item
class Shu1701Spider(scrapy.Spider):
    name = 'shu1701'
    # allowed_domains = ['www.jianshu.com']
    # start_urls = ['http://www.jianshu.com/']
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    def start_requests(self):
        url = 'http://www.jianshu.com/'
        yield Request(url=url,headers=self.header)
    def parse(self, response):
        lis = response.xpath('//*[@id="list-container"]/ul/li[@class="have-img"]')
        for li in lis:
            item = Book1701Item()
            item['titles'] = li.xpath('div/a/text()').extract()
            item['links'] = li.xpath('div/a/@href').extract()
            item['contents'] = li.xpath('div/p/text()').extract()
            yield item
