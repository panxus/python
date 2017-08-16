# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader
import re
import hashlib
import time

def date_handle(val):
    date =val.replace('·','').strip()
    try:
        s = time.mktime(time.strptime(date,'%Y/%m/%d'))
    except Exception as e:
        return 0
    else:
        return s


def fav_handle(val):
    s = re.match(r'(\d+)',val)
    return s.group(1) if s else 0


def tag_handle(val):
    if '评论' in val:
        return ''
    else:
        return val

def get_md5(val):
    if isinstance(val,str):
        val = val.encode('utf-8')
    m = hashlib.md5()
    m.update(val)
    return m.hexdigest()


def image_handle(val):
    return val


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class BoleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_handle),
        # output_processor=TakeFirst()
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field(
        input_processor=MapCompose(get_md5)
    )
    front_image_url = scrapy.Field(
        output_processor=MapCompose(image_handle)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    fav_nums = scrapy.Field(
        input_processor=MapCompose(fav_handle)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(fav_handle)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(tag_handle),
        output_processor=Join(",")
    )
    content = scrapy.Field()
