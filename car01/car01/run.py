#coding=utf-8
#切换spider 需修改对应的pipeline
from scrapy import cmdline

name_1 = 'c01'
name_2 = 'c02'

cmd = 'scrapy crawl %s' % name_1

cmdline.execute(cmd.split())