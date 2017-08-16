from scrapy.cmdline import execute

name = 'bl'

code = 'scrapy crawl {0}'.format(name)

execute(code.split())