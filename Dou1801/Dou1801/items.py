# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Dou1801Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    ranks = scrapy.Field()
    titles = scrapy.Field()
    score = scrapy.Field()
    nums = scrapy.Field()
    des = scrapy.Field()
    links = scrapy.Field()


class Dou1802Item(scrapy.Item):
    titles = scrapy.Field()
    score = scrapy.Field()
    pass
