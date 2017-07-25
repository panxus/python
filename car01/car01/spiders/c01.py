# -*- coding: utf-8 -*-
import scrapy
from car01.items import Car01Item

class C01Spider(scrapy.Spider):
    name = 'c01'
    start_urls = ['http://www.autohome.com.cn/car/']

    def parse(self, response):
        dls = response.xpath('//*[@id="contentSeries"][1]/dl[position()>1]')
        for dl in dls:
            dds = dl.xpath('dd')
            for dd in dds:
                item = Car01Item()
                item['brand_index'] = dd.xpath('a/@eng').extract()[0]
                item['brand_id'] = dd.xpath('a/@vos').extract()[0]
                item['brand_name'] = dd.xpath('a/@cname').extract()[0]
                item['brand_logo'] = dd.xpath('a/em/img/@src').extract()
                yield item
