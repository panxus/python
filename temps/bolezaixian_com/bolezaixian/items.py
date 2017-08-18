# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,Join,TakeFirst
from bolezaixian.utils.common import date_handle,url_handle,ob_handle,nums_handle


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


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




class ZhiHuQuestionItem(scrapy.Item):
    question_id=scrapy.Field()
    question_url=scrapy.Field()
    question_title=scrapy.Field()
    question_topic=scrapy.Field(
        output_processor = Join(',')
    )
    question_content=scrapy.Field()
    question_pinglun=scrapy.Field(
        input_processor=MapCompose(nums_handle)
    )
    question_huida=scrapy.Field(
        input_processor=MapCompose(nums_handle)
    )
    question_guanzhu=scrapy.Field()


class ZhiHuAnswerItem(scrapy.Item):
    pass