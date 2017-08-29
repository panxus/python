# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        # Rule(LinkExtractor(allow=('zhaopin/.*',))),
        # Rule(LinkExtractor(allow=(r'gongsi/j\d+.html',))),
        Rule(LinkExtractor(allow=(r'jobs/\d+.html',)), callback='parse_job', follow=True),
    )

    def parse_job(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
