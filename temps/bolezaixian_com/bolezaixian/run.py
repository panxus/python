from scrapy.cmdline import execute

#伯乐在线
# name = 'blzz_spider'

#知乎
name = 'zht'


execute(['scrapy','crawl',name])


