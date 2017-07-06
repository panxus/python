#coding=utf-8
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
url = 'http://so.gushiwen.org/gushi/songsan.aspx'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Referer':'http://www.gushiwen.org/'}
cont = requests.get(url,headers=headers).content
soup = BeautifulSoup(cont,'lxml')
result = soup.find_all('span')
last = []
for i in result:
    flag = {}
    flag['href'] = i.a.attrs['href']
    flag['title']= i.a.string
    if len(i.contents) == 2:
        flag['author']=i.contents[1]
    else:
        flag['author']='null'
    last.append(flag)
head = 'length:'+ str(len(last))+'\n'
f = open('ci.txt','wb')
f.write(head)
start = '--------------start--------------'
for i in last:
    str = '标题:{0}\n作者:{1}\n地址:{2}\n'.format((i['title']),(i['author']),(i['href']))
    f.write(str)
    f.write('---------------------------------\n')
end = '--------------end--------------'
f.write(end)
f.close()