# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,Join,TakeFirst
import time
import hashlib
import re


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def date_handle(val):
    vals = val.replace('·','').strip()
    try:
        s = time.mktime(time.strptime(vals,'%Y/%m/%d'))
    except Exception as e:
        return 0
    else:
        return int(s)


def url_handle(val):
    return val


def ob_handle(url):
    if isinstance(url,str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def nums_handle(val):
    s = re.search('(\d+)',val)
    if s:
        return s.group(1)
    else:
        return 0


class BolezaixianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_handle)
    )
    tags = scrapy.Field(
        output_processor=Join(',')
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field(
        input_processor=MapCompose(ob_handle)
    )
    image_url = scrapy.Field(
        output_processor=MapCompose(url_handle)
    )
    image_path = scrapy.Field()
    z_num = scrapy.Field()
    sc_num = scrapy.Field(
        input_processor=MapCompose(nums_handle)
    )
    pl_num = scrapy.Field(
        input_processor=MapCompose(nums_handle)
    )
