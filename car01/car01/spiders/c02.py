# -*- coding: utf-8 -*-
import scrapy
from car01.items import Car02Item

class C02Spider(scrapy.Spider):
    name = 'c02'
    # allowed_domains = ['autohome.com']
    # start_urls = ['http://www.autohome.com.cn/grade/carhtml/A.html']

    def start_requests(self):
        start_url = 'http://www.autohome.com.cn/grade/carhtml/%s.html'
        for i in xrange(26):
            si = chr(i + ord('A'))
            real_url = start_url % si
            yield scrapy.Request(real_url)
        # yield scrapy.Request(url='http://www.autohome.com.cn/grade/carhtml/A.html')

    def parse(self, response):
        dls = response.xpath('//dl')
        # print dls
        for dl in dls:
            brand_id = dl.xpath('@id').extract()[0]
            brand_name = dl.xpath('dt/div/a/text()').extract()[0]
            uls = dl.xpath('dd/ul')
            for i,ul in enumerate(uls):
                l = dl.xpath('dd/div[@class="h3-tit"]['+str(i+1)+']/text()').extract()[0]
                lis = ul.xpath('li[@id]')
                for li in lis:
                    cFlag = Car02Item()
                    cFlag['series_name'] = li.xpath('h4/a/text()').extract()[0]
                    cFlag['series_id'] = li.xpath('@id').re(r'\d+')[0]
                    cFlag['series_url'] = li.xpath('h4/a/@href').extract()[0]
                    cFlag['guide_price'] = li.xpath('div[1]/a/text()').extract()[0]
                    cFlag['factory'] = l
                    cFlag['brand_id'] = brand_id
                    cFlag['brand_name'] = brand_name
                    yield cFlag


