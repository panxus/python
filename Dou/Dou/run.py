from scrapy import cmdline

name = 'dbooks'

code = "scrapy crawl {0}".format(name)
# code = "scrapy crawl {0} -o book.csv".format(name)

cmdline.execute(code.split())