from scrapy import cmdline

name = 'zol_2'

cmd = 'scrapy crawl {0}'.format(name)

cmdline.execute(cmd.split())