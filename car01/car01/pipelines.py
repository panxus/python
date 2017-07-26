# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

import MySQLdb
#spider c01
class Car01Pipeline(object):

    def process_item(self, item, spider):
        args = spider.settings.get('DBCONFIG')
        con = MySQLdb.connect(**args)
        cur = con.cursor()
        sql = ("insert into car_brand (brand_index,brand_id,brand_name,brand_logo)"
               "values(%s,%s,%s,%s)")
        data = (item['brand_index'],item['brand_id'],item['brand_name'],item['image_paths'][0])
        cur.execute(sql,data)
        con.commit()
        cur.close()
        con.close()
        return item

#spider c01
class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)

    def get_media_requests(self, item, info):
        for image_url in item['brand_logo']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item




#spider c02

class Car02Pipeline(object):

    def process_item(self, item, spider):
        args = spider.settings.get('DBCONFIG')
        con = MySQLdb.connect(**args)
        cur = con.cursor()

        sql = ("insert into car_series (brand_id,brand_name,series_id,series_name,series_url,guide_price,factory)"
               "values(%s,%s,%s,%s,%s,%s,%s)")
        data = (item['brand_id'],item['brand_name'],item['series_id'],item['series_name'],item['series_url'],item['guide_price'],item['factory'])
        cur.execute(sql,data)
        con.commit()
        cur.close()
        con.close()
        return item