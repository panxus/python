# -*- coding: utf-8 -*-
import scrapy
from Dou.items import DouItem

class DbooksSpider(scrapy.Spider):
    name = 'dbooks'
    # allowed_domains = ['www.douban.com']
    # start_urls = ['http://www.douban.com/']
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    def start_requests(self):
        url = 'https://www.douban.com/doulist/1264675/'
        yield scrapy.Request(url=url,headers=self.headers)
    def parse(self,response):
        book_divs = response.xpath('//div[@class="doulist-item"]')
        for book in book_divs:
            item = DouItem()
            item['rank'] = book.xpath('div/div[1]/span/text()').extract()[0]
            item['name'] = book.xpath('div/div[2]/div[3]/a/text()').extract()[0].strip()
            item['link'] = book.xpath('div/div[2]/div[3]/a/@href').extract()[0]
            item['score'] = book.xpath('div/div[2]/div[4]/span[2]/text()').extract()[0]
            yield item

