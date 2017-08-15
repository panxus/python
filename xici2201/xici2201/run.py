from scrapy import cmdline

# name = 'xc2202'
name = 'kdl_2'

cmd = 'scrapy crawl {0}'.format(name)

cmdline.execute(cmd.split())