#coding=utf-8
from scrapy import cmdline

# 调试方法②
name = 'Movie1801'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())