# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import parse
from bolezaixian.items import BolezaixianItem

class BlzzSpiderSpider(scrapy.Spider):
    name = 'blzz_spider'
    allowed_domains = ['blog.jobbole.com']
    # 'http://blog.jobbole.com/all-posts/',
    start_urls = ['http://blog.jobbole.com/all-posts/page/549/']

    def parse(self, response):
        div_box = response.xpath('//div[@id="archive"]/div[contains(@class,"floated-thumb")]')
        for div in div_box:
            a_url = div.xpath('div[2]/p[1]/a[1]/@href').extract_first('')
            img_url = div.xpath('div[1]/a/img/@src').extract_first('')
            yield Request(parse.urljoin(response.url,a_url),meta={'image_url':img_url},callback=self.parse_detail)

    def parse_detail(self,response):
        item = BolezaixianItem()
        item['title'] = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('')
        item['content'] = response.xpath('//div[@class="entry"]').extract_first('')
        item['url'] = response.url
        item['create_date'] = response.xpath('//div[@class="entry-meta"]/p/text()').extract_first('').replace('·','').strip()
        tag_list = response.xpath('//div[@class="entry-meta"]/p/a/text()').extract()
        tags = [i for i in tag_list if not i.strip().endswith('评论')]
        item['tags'] = ''.join(tags)
        item['image_url'] = [parse.urljoin(response.url,response.meta.get('image_url'))]

        item['z_num'] = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract_first('')
        sc_num = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').re('\d+')
        item['sc_num'] = sc_num[0] if sc_num else 0
        pl_num = response.xpath('//span[contains(@class,"hide-on-480")]/text()').re('\d+')
        item['pl_num'] = pl_num[0] if pl_num  else 0
        yield item