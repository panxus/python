# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BolezaixianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    create_date = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    image_path = scrapy.Field()
    z_num = scrapy.Field()
    sc_num = scrapy.Field()
    pl_num = scrapy.Field()
