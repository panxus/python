# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import parse
from bole.items import BoleItem,ArticleItemLoader

# from scrapy.loader import ItemLoader

class BlSpider(scrapy.Spider):
    name = 'bl'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        nodes = response.css('#archive .floated-thumb .post-thumb a')
        for node in nodes:
            url = node.css('::attr(href)').extract_first('')
            front_images_url = node.css('img::attr(src)').extract_first('')
            yield Request(url=parse.urljoin(response.url,url),callback=self.parse_datail,meta={'front_images_url':front_images_url})

    def parse_datail(self, response):
        # item = BoleItem()
        # front_image_url = response.meta.get('front_images_url','')
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        # create_date = response.xpath('//div[@class="entry-meta"]/p/text()').extract()[0].replace('·','').strip()
        # praise_nums = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract_first(0)
        # favs = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').re('(\d+)')
        # fav_nums = favs[0] if favs else 0
        # comments = response.xpath('//span[contains(@class,"hide-on-480")]/text()').re('(\d+)')
        # comment_nums = comments[0] if comments else 0
        # tagss = response.xpath('//div[@class="entry-meta"]/p/a/text()').extract()
        # tags_list = [e for e in tagss if not e.strip().endswith('评论')]
        # tags = ','.join(tags_list)
        # content = response.css('div.entry').extract()[0]
        # item['title'] = title
        # item['url'] = response.url
        # item['url_object_id'] = get_md5(response.url)
        # item['create_date'] = create_date
        # item['front_image_url'] = [front_image_url]
        # item['praise_nums'] = praise_nums
        # item['fav_nums'] = fav_nums
        # item['comment_nums'] = comment_nums
        # item['tags'] = tags
        # item['content'] = content

        # 通过itemloader加载item
        item_loader = ArticleItemLoader(item=BoleItem(),response=response)
        item_loader.add_xpath('title','//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath('create_date','//div[@class="entry-meta"]/p/text()')
        item_loader.add_xpath('praise_nums','//span[contains(@class,"vote-post-up")]/h10/text()')
        item_loader.add_xpath('fav_nums','//span[contains(@class,"bookmark-btn")]/text()')
        item_loader.add_xpath('comment_nums','//span[contains(@class,"hide-on-480")]/text()')
        item_loader.add_xpath('tags','//div[@class="entry-meta"]/p/a/text()')
        item_loader.add_css('content','div.entry')
        item_loader.add_value('front_image_url',response.meta.get('front_images_url',''))
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_object_id',response.url)

        article_item = item_loader.load_item()
        yield article_item