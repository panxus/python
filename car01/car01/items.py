# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Car01Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand_index = scrapy.Field()
    brand_id = scrapy.Field()
    brand_name = scrapy.Field()
    brand_logo = scrapy.Field()
    image_paths = scrapy.Field()
    car_url = scrapy.Field()
    pass
