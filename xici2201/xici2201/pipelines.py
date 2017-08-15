# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

user = 'root'
passwd='root'
port=3307
db='tp_blog'
host='127.0.0.1'
import pymysql

class Xici2201Pipeline(object):
    def __init__(self):
        self.con = pymysql.connect(host=host,user=user,passwd=passwd,port=port,db=db,charset='utf8')
        self.cur = self.con.cursor()

        self.cur.execute('delete from erp_ip;')
        self.con.commit()

    def process_item(self, item, spider):
        self.cur.execute(''' insert into erp_ip (ip,port,address,niming,type,speed,link_time,live_time,ver_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) ''',
                         (
                             item['ip'],
                             item['port'],
                             item['address'],
                             item['niming'],
                             item['type'],
                             item['speed'],
                             item['link_time'],
                             item['live_time'],
                             item['ver_time'],
                         )
                         )
        self.con.commit()
        return item
