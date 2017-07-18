# -*- coding: utf-8 -*-
import scrapy
from Dou1801.items import Dou1801Item

class Movie1801Spider(scrapy.Spider):
    name = 'Movie1801'
    headers = {'Host':'movie.douban.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield scrapy.Request(url=url,headers=self.headers)

    def parse(self, response):

        # #调试
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        # # shell >> view(response)

        lis = response.xpath('//ol[@class="grid_view"]/li')
        for li in lis:
            item = Dou1801Item()
            item['ranks'] = li.xpath('div/div[1]/em/text()').extract()[0]
            item['titles'] = li.xpath('div/div[2]/div[1]/a/span[1]/text()').extract()[0]
            item['score'] = li.xpath('div/div[2]/div[2]/div/span[2]/text()').extract()[0]
            item['nums'] = li.xpath('div/div[2]/div[2]/div/span[4]/text()').extract()[0]
            des = li.xpath('div/div[2]/div[2]/p[2]/span/text()').extract()
            if des:
                item['des'] = des[0]
            item['links'] = li.xpath('div/div[2]/div[1]/a/@href').extract()[0]
            yield item

        next_url = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield scrapy.Request(url=next_url,headers=self.headers)
