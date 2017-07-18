# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class Dou1801Pipeline(object):
    def process_item(self, item, spider):
        return item




class DouSavePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='root', db='jr_car', host='127.0.0.1', charset="utf8", use_unicode=True,port=3307)
        self.cursor = self.conn.cursor()
        #清空表：
        self.cursor.execute("truncate table erp_movie;")
        self.conn.commit()
    def process_item(self, item, spider):
        try:
            self.cursor.execute("""INSERT INTO erp_movie (score, links, nums, ranks, des, titles)  
                                VALUES (%s, %s, %s, %s, %s, %s)""",
                                (
                                    item['score'].encode('utf-8'),
                                    item['links'].encode('utf-8'),
                                    item['nums'].encode('utf-8'),
                                    item['ranks'].encode('utf-8'),
                                    item['des'].encode('utf-8'),
                                    item['titles'].encode('utf-8'),
                                )
                                )

            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item