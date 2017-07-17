# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Book1701Pipeline(object):
    def process_item(self, item, spider):
        # return item

        # for i in item:
        i = item
        title = i['titles'][0]
        link = i['links'][0]
        content = i['contents'][0]
        fname = file('jianshu.txt','a')
        cons = 'title: %s,link: %s,title:%s \n' % (title,link,content)
        fname.write(cons)
        fname.write('-----------\n')
        fname.close()