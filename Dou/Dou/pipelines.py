# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
host = '127.0.0.1'
user = 'root'
pd = ""
db = 'jr_car'
port=3306

class DouPipeline(object):
    def __init__(self):
        self.con = MySQLdb.connect(host=host,user=user,passwd=pd,db=db,charset="utf8", use_unicode=True,port=port)
        self.cur = self.con.cursor()

        self.cur.execute('delete from erp_book;')
        self.con.commit()
        pass

    def process_item(self, item, spider):

        try:

            self.cur.execute(""" insert into erp_book (rank,name,link,score) values (%s,%s,%s,%s) """,
                             (
                                 item['rank'],
                                 item['name'],
                                 item['link'],
                                 item['score'],

                             ))
            self.con.commit()

        except MySQLdb.Error,e:
            print e.args[0],e.args[1]

        return item

