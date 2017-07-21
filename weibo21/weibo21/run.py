from scrapy import cmdline

name = 'wapweibo2'

cmd = 'scrapy crawl {0}'.format(name)

cmdline.execute(cmd.split())