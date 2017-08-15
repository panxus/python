# -*- coding: utf-8 -*-
import scrapy
from xici2201.items import Xici2201Item

class Xc2201Spider(scrapy.Spider):
    name = 'kdl_2'
    # str_page = raw_input('输入抓取页数开始:\n')
    # max_page = raw_input('输入抓取页数结束:\n')
    str_page = 1
    max_page = 1

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    begin_url = 'http://www.kuaidaili.com/free/inha/%d/'

    def start_requests(self):
        url = self.begin_url % int(self.str_page)
        yield scrapy.Request(url=url,headers=self.headers)

    def parse(self, response):
        trs = response.xpath('//*[@id="list"]/table/tbody/tr')
        for tr in trs:
            item = Xici2201Item()
            item['ip'] = tr.xpath('td[1]/text()').extract()[0]
            item['port'] = tr.xpath('td[2]/text()').extract()[0]
            address = tr.xpath('td[5]/a/text()').extract()
            if address:
                item['address'] = address[0]
            else:
                item['address'] = ''
            item['niming'] = tr.xpath('td[3]/text()').extract()[0]
            item['type'] = tr.xpath('td[4]/text()').extract()[0]
            item['speed'] = tr.xpath('td[6]/div/@title').re(r'\d{0,2}\.\d{0,}')[0]
            item['link_time'] = tr.xpath('td[7]/div/@title').re(r'\d{0,2}\.\d{0,}')[0]
            item['live_time'] = ''
            item['ver_time'] = ''
            yield item

        now_page = response.xpath('//a[@class="active"]/text()').extract()[0]

        next_url = self.begin_url % (int(now_page)+1)

        if int(now_page) <= int(self.max_page):
            yield scrapy.Request(next_url,headers=self.headers)
