# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import parse
from bolezaixian.items import BolezaixianItem,ArticleItemLoader

class BlzzSpiderSpider(scrapy.Spider):
    name = 'blzz_spider'
    allowed_domains = ['blog.jobbole.com']
    # 'http://blog.jobbole.com/all-posts/',
    start_urls = ['http://blog.jobbole.com/all-posts/page/1/']

    custom_settings = {
        'ITEM_PIPELINES':{
            'bolezaixian.pipelines.BlogArticlePipeline': 30,
            'bolezaixian.pipelines.MysqlTwistedPipeline': 60,
        }
    }

    def parse(self, response):
        div_box = response.xpath('//div[@id="archive"]/div[contains(@class,"floated-thumb")]')
        for div in div_box:
            a_url = div.xpath('div[2]/p[1]/a[1]/@href').extract_first('')
            img_url = div.xpath('div[1]/a/img/@src').extract_first('')
            yield Request(parse.urljoin(response.url,a_url),meta={'image_url':img_url},callback=self.parse_detail)

        #下一页
        # next_url = response.xpath('//a[contains(@class,"next")]/@href').extract_first()
        # if next_url:
        #     yield Request(next_url,callback=self.parse)


    def parse_detail(self,response):

        item_loader=ArticleItemLoader(item=BolezaixianItem(),response=response)
        item_loader.add_xpath('title','//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath('content','//div[@class="entry"]')
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_object_id',response.url)
        item_loader.add_xpath('create_date','//div[@class="entry-meta"]/p/text()')
        item_loader.add_xpath('tags','//div[@class="entry-meta"]/p/a/text()')
        item_loader.add_value('image_url',parse.urljoin(response.url,response.meta.get('image_url')))
        item_loader.add_xpath('z_num','//span[contains(@class,"vote-post-up")]/h10/text()')
        item_loader.add_xpath('sc_num','//span[contains(@class,"bookmark-btn")]/text()')
        item_loader.add_xpath('pl_num','//span[contains(@class,"hide-on-480")]/text()')
        item = item_loader.load_item()
        return item