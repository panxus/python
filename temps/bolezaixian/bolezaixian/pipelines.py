# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter
import codecs
import json
import pymysql

class BolezaixianPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonFilePipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')
        self.file.write('[')

    def process_item(self, item, spider):
        # 中文
        lines = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(lines)
        return item

    def close_spider(self,spider):
        self.file.write(']')
        self.file.close()

class JsonExporter(object):
    #调用jsonexporter到处json文件
    def __init__(self):
        self.file = open('articleexporter.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()


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


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        path = [j['path'] for i,j in results if i]
        if not path:
            raise DropItem('no images')
        item['front_image_path'] = path
        return item