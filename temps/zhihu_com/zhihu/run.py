from scrapy.cmdline import execute

name = 'zh'

order = 'scrapy crawl %s' % name

execute(order.split())