from scrapy import cmdline

name = 'c01'

cmd = 'scrapy crawl %s' % name

cmdline.execute(cmd.split())