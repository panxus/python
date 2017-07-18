# -*- coding: utf-8 -*-
import scrapy
import json
from Dou1801.items import Dou1802Item

class Movie1802Spider(scrapy.Spider):
    name = 'Movie1802'
    headers = {'Host':'movie.douban.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    def start_requests(self):
        url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=0'
        yield scrapy.Request(url=url,headers=self.headers)

    def parse(self, response):
        re = response.body
        data =  json.loads(re)
        item = Dou1802Item()
        if data:
            for da in data['data']:
                item['titles'] = da['title']
                item['score'] = da['rate']
                yield item


            #有数据则采集下一页
            import re
            page_num = re.search(r'start=(\d+)',response.url).group(1)
            #限制
            if int(page_num) <=100:
                new_page = 'start='+str(int(page_num)+20)
                next_url = re.sub(r'start=\d+',new_page,response.url)
                yield scrapy.Request(url=next_url,headers=self.headers)

