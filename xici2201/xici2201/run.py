from scrapy import cmdline

name = 'xc2202'

cmd = 'scrapy crawl {0}'.format(name)

cmdline.execute(cmd.split())