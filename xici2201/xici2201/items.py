# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Xici2201Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
    address = scrapy.Field()
    niming = scrapy.Field()
    type = scrapy.Field()
    speed = scrapy.Field()
    link_time = scrapy.Field()
    live_time = scrapy.Field()
    ver_time = scrapy.Field()
