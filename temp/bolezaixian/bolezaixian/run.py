from scrapy.cmdline import execute

name = 'blzx_spider'

code = 'scrapy crawl {0}'.format(name)

execute(code.split())