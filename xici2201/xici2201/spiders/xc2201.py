# -*- coding: utf-8 -*-
import scrapy
from xici2201.items import Xici2201Item

class Xc2201Spider(scrapy.Spider):
    name = 'xc2202'
    max_page = raw_input('输入抓取页数:\n')
    # allowed_domains = ['xici.com']
    # start_urls = ['http://www.xicidaili.com/nn/']
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    begin_url = 'http://www.xicidaili.com/nn/%d'

    def start_requests(self):
        url = self.begin_url % 1
        yield scrapy.Request(url=url,headers=self.headers)

    def parse(self, response):
        trs = response.xpath('//*[@id="ip_list"]/tr[position()>1]')
        # trs = response.xpath('//*[@id="ip_list"]/tr[2]')
        for tr in trs:
            item = Xici2201Item()
            item['ip'] = tr.xpath('td[2]/text()').extract()[0]
            item['port'] = tr.xpath('td[3]/text()').extract()[0]
            address = tr.xpath('td[4]/a/text()').extract()
            if address:
                item['address'] = address[0]
            else:
                item['address'] = ''
            item['niming'] = tr.xpath('td[5]/text()').extract()[0]
            item['type'] = tr.xpath('td[6]/text()').extract()[0]
            item['speed'] = tr.xpath('td[7]/div/@title').re(r'\d{0,2}\.\d{0,}')[0]
            item['link_time'] = tr.xpath('td[8]/div/@title').re(r'\d{0,2}\.\d{0,}')[0]
            item['live_time'] = tr.xpath('td[9]/text()').extract()[0]
            item['ver_time'] = tr.xpath('td[10]/text()').extract()[0]
            yield item

        next_url = response.xpath('//a[@class="next_page"]/@href').extract()[0]
        num = next_url.split('/')[-1]
        if next_url and int(num) <= int(self.max_page):
            yield scrapy.Request(response.urljoin(next_url),headers=self.headers)
