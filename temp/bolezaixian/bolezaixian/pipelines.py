# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BolezaixianPipeline(object):
    def process_item(self, item, spider):
        return item



from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class BlogArticlePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        # node = info.downloaded
        # for n in node:
        #     item['image_path'] = node[n]['path']

        image = [y['path'] for x,y in results if x]
        if not image:
            raise DropItem('no images')
        item['image_path'] = image
        return item
