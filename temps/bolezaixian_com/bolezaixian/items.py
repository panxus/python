# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,Join,TakeFirst
from bolezaixian.utils.common import date_handle,url_handle,ob_handle,nums_handle,get_now_unix


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class BolezaixianItem(scrapy.Item):

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

    def getItemSql(self):

        sql = '''
            INSERT INTO article_spider (title, create_date, url, url_object_id, image_url, image_path, z_num, sc_num, pl_num, tags, content)
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update z_num = VALUES (z_num),sc_num = VALUES (sc_num),pl_num = VALUES (pl_num),content = VALUES (content)
        '''
        image_url = self['image_url'][0] if self['image_url'] else ''
        image_path = self['image_path'][0] if self['image_path'] else ''
        data = (self['title'], self['create_date'], self['url'], self['url_object_id'], image_url, image_path, self['z_num'], self['sc_num'], self['pl_num'], self['tags'], self['content'])
        return sql,data


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

    def getItemSql(self):
        sql = ''' insert into zh_question (question_id,question_url,question_title,question_topic,question_content,question_pinglun,question_huida,question_guanzhu) values (%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update question_pinglun = VALUES (question_pinglun),question_huida= VALUES (question_huida),question_guanzhu= values (question_guanzhu)'''
        data = (self['question_id'],self['question_url'],self['question_title'],self['question_topic'],self['question_content'],self['question_pinglun'],self['question_huida'],self['question_guanzhu'])
        return sql,data


class ZhiHuAnswerItem(scrapy.Item):
    answer_id = scrapy.Field()
    question_id = scrapy.Field()
    created = scrapy.Field()
    updated = scrapy.Field()
    crawl = scrapy.Field(
        output_processor=MapCompose(get_now_unix)
    )
    answer_content = scrapy.Field()
    answer_excerpt = scrapy.Field()
    answer_author_name = scrapy.Field()
    answer_author_id = scrapy.Field()
    answer_pl = scrapy.Field()
    def getItemSql(self):
        sql = ''' insert into zh_answer (answer_id,question_id,created,updated,crawl,answer_content,answer_excerpt,answer_author_name,answer_author_id,answer_pl) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update updated = VALUES (updated),crawl= VALUES (crawl),answer_content= values (answer_content),answer_excerpt = VALUES (answer_excerpt),answer_pl = VALUES (answer_pl)'''
        data = (self['answer_id'],self['question_id'],self['created'],self['updated'],self['crawl'],self['answer_content'],self['answer_excerpt'],self['answer_author_name'],self['answer_author_id'],self['answer_pl'])
        return sql,data
