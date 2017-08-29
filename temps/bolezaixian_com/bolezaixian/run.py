from scrapy.cmdline import execute

#伯乐在线
# name = 'blzz_spider'

#知乎
# name = 'zht'

# 拉钩
name = 'lagou'

execute(['scrapy','crawl',name])


