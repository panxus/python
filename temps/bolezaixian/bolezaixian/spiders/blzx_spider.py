# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from bolezaixian.items import BoleArticleItem
from bolezaixian.utils.common import get_md5

class BlzxSpiderSpider(scrapy.Spider):
    name = 'blzx_spider'
    allowed_domains = ['blog.jobbole.com']
    # start_urls = ['http://blog.jobbole.com/all-posts/page/1/']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        nodes = response.css('#archive .floated-thumb .post-thumb a')
        for node in nodes:
            url = node.css('::attr(href)').extract_first('')
            front_images_url = node.css('img::attr(src)').extract_first('')
            yield Request(url=parse.urljoin(response.url,url),callback=self.parse_datail,meta={'front_images_url':front_images_url})

        # next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first('')
        # if next_url:
        #     yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)

    def parse_datail(self, response):
        item = BoleArticleItem()

        front_image_url = response.meta.get('front_images_url','')
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        create_date = response.xpath('//div[@class="entry-meta"]/p/text()').extract()[0].replace('·','').strip()

        praise_nums = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract_first('')
        favs = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').re('(\d+)')
        if favs:
            fav_nums = favs[0]
        else:
            fav_nums = 0
        comments = response.xpath('//span[contains(@class,"hide-on-480")]/text()').re('(\d+)')
        if comments:
            comment_nums = comments[0]
        else:
            comment_nums = 0
        tagss = response.xpath('//div[@class="entry-meta"]/p/a/text()').extract()
        tags_list = [e for e in tagss if not e.strip().endswith('评论')]
        tags = ','.join(tags_list)

        content = response.css('div.entry').extract()[0]

        item['title'] = title
        item['url'] = response.url
        item['url_object_id'] = get_md5(response.url)
        item['create_date'] = create_date
        item['front_image_url'] = [front_image_url]
        item['praise_nums'] = praise_nums
        item['fav_nums'] = fav_nums
        item['comment_nums'] = comment_nums
        item['tags'] = tags
        item['content'] = content
        yield item