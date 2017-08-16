# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import pymysql
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
class BolePipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
       if 'front_image_url' in item:
           path = [v['path'] for k,v in results if k]
           if not path:
               path = ''
       else:
           path = ''
       item['front_image_path'] = path
       return item


class MysqlSavePipeline(object):
    def process_item(self, item, spider):
        arg = spider.settings.get('DBCONFIG')
        self.con = pymysql.connect(**arg)
        self.cur = self.con.cursor()
        sql = '''
            insert into article_spider (title,create_date,url,url_object_id,front_image_url,front_image_path,praise_nums,fav_nums,comment_nums,tags,content)
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
       '''
        front_image_path = item['front_image_path'][0] if item['front_image_path'] else ''
        front_image_url = item['front_image_url'][0] if item['front_image_url'] else ''
        data  = (item['title'],item['create_date'],item['url'],item['url_object_id'],front_image_url,front_image_path,item['praise_nums'],item['fav_nums'],item['comment_nums'],item['tags'],item['content'])
        self.cur.execute(sql,data)
        self.con.commit()
        return item

class JsonSavePipeline(object):
    def __init__(self):
        self.file = open('articlejson.json','wb')
        self.exp = JsonItemExporter(self.file,encoding=None,ensure_ascii=False)
        self.exp.start_exporting()
    def process_item(self, item, spider):
        self.exp.export_item(item)
        return item

    def close_spider(self,spider):
        self.exp.finish_exporting()
        self.file.close()


class MysqlIoSavePipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):
        args = settings.get('DBCONFIG')
        dbpool = adbapi.ConnectionPool('pymysql',**args)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.hand_data,item)
        query.addErrback(self.error_func)
        return item

    def error_func(self,fail):
        print(fail)

    def hand_data(self,cursor,item):
        sql = '''
            insert into article_spider (title,create_date,url,url_object_id,front_image_url,front_image_path,praise_nums,fav_nums,comment_nums,tags,content)
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
       '''
        front_image_path = item['front_image_path'][0] if item['front_image_path'] else ''
        front_image_url = item['front_image_url'][0] if item['front_image_url'] else ''
        data  = (item['title'],item['create_date'],item['url'],item['url_object_id'],front_image_url,front_image_path,item['praise_nums'],item['fav_nums'],item['comment_nums'],item['tags'],item['content'])
        cursor.execute(sql,data)



