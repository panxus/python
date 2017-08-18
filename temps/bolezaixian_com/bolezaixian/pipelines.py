# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

class BolezaixianPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonExporter(object):
    def __init__(self):
        self.file = open('article.json','wb')
        self.expo = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.expo.start_exporting()

    def process_item(self, item, spider):
        self.expo.export_item(item)
        return item

    def close_spider(self, spider):
        self.expo.finish_exporting()
        self.file.close()


class MysqlSavePipeline(object):
    #采用同步写入数据
    def process_item(self, item, spider):
        arg = spider.settings.get('MYSQLDB')
        self.con = pymysql.connect(**arg)
        self.cur = self.con.cursor()
        sql = '''
            INSERT INTO article_spider (title, create_date, url, url_object_id, image_url, image_path, z_num, sc_num, pl_num, tags, content)
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        image_url = item['image_url'][0] if item['image_url'] else ''
        image_path = item['image_path'][0] if item['image_path'] else ''
        data = (item['title'], item['create_date'], item['url'], item['url_object_id'], image_url, image_path, item['z_num'], item['sc_num'], item['pl_num'], item['tags'], item['content'])
        self.cur.execute(sql,data)
        self.con.commit()
        return item



class MysqlTwistedPipeline(object):
    #采用异步写入数据
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):
        args = settings['MYSQLDB']
        # args['cursorclass'] = pymysql.cursors.DictCursor
        dbpool = adbapi.ConnectionPool('pymysql',**args)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)
        return item

    def handle_error(self,failure):
        print(failure)

    def do_insert(self,cursor,item):
        sql = '''
            INSERT INTO article_spider (title, create_date, url, url_object_id, image_url, image_path, z_num, sc_num, pl_num, tags, content)
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        image_url = item['image_url'][0] if item['image_url'] else ''
        image_path = item['image_path'][0] if item['image_path'] else ''
        data = (item['title'], item['create_date'], item['url'], item['url_object_id'], image_url, image_path, item['z_num'], item['sc_num'], item['pl_num'], item['tags'], item['content'])
        cursor.execute(sql,data)



class BlogArticlePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):

        image = [y['path'] for x,y in results if x]
        # if not image:
        #     raise DropItem('no images')
        item['image_path'] = image
        return item
