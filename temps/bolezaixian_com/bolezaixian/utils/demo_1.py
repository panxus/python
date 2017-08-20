import requests
from lxml import etree

#
# rq = requests.get('https://stackoverflow.com/questions')
# html = etree.HTML(rq.content)
# s = html.xpath('//a[contains(@href,"/questions/")]/@href')
# print(s)

head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'}
s = requests.get('https://www.lagou.com/jobs/3390430.html',headers=head)

print(s.status_code)
print(s.content)

