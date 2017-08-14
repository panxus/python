#coding=utf-8
import requests
from bs4 import BeautifulSoup
import sys
import urlparse
import os
reload(sys)
sys.setdefaultencoding('utf-8')

class BiquTest1(object):

    def __init__(self,url):
        self.url = url
        self.books_1 = []
        self.dir = 'books_'

    def _getHtml(self,url):
        try:
            req = requests.get(url,timeout=20)
            req.raise_for_status()
            req.encoding = req.apparent_encoding
        except Exception,e:
            print '地址请求失败:',e
        else:
            return req.text


    def _parseW(self,html):
        soup = BeautifulSoup(html,'lxml')

        box_1 = soup.find_all('div',class_="index_toplist mright mbottom")
        flag = {}
        for box in box_1:
            flag['type'] = box.find('div',class_='toptab').span.string
            book = box.find('div',attrs={'class':'topbooks','style':'display: block;'})
            lis = book.find_all('li')
            flag['book'] = []
            for li in lis:
                index = li.find('span',class_='num').string
                href = li.a['href']
                l_href = urlparse.urljoin(self.url,href)
                name = li.a.string
                flag['book'].append({'name':index+name,'href':l_href})
            self.books_1.append(flag)
            flag = {}

        box_2 = soup.select('div[class="index_toplist mbottom"]')
        for box in box_2:
            flag['type'] = box.find('div',class_='toptab').span.string
            book = box.find('div',attrs={'class':'topbooks','style':'display: block;'})
            lis = book.find_all('li')
            flag['book'] = []
            for li in lis:
                index = li.find('span',class_='num').string
                href = li.a['href']
                l_href = urlparse.urljoin(self.url,href)
                name = li.a.string
                flag['book'].append({'name':index+name,'href':l_href})
            self.books_1.append(flag)
            flag = {}

    def _downDetail(self):
        if self.books_1:
            if not os.path.isdir(self.dir):
                os.mkdir(self.dir)
            with file(self.dir+'/book_all.txt','a+') as f:
                for li in self.books_1:
                    f.write(li['type']+':\n')
                    for bk in li['book']:
                        f.write('{0},地址:{1}.\n'.format(bk['name'],bk['href']))
                    f.write('\n\n')
                f.close()


    def _downAllBooks(self):
        if self.books_1:
            for li in self.books_1:
                for book in li['book']:
                    self._downCap(book)


    def _downCap(self,book):
        html = self._getHtml(book['href'])
        soup = BeautifulSoup(html,'lxml')
        dd = soup.select('div#list > dl > dd')
        with open(self.dir+'/'+book['name']+'.txt','a+') as f:
            for a in dd:
                cap_name = a.a.string
                cap_con = self._downCapCon(urlparse.urljoin(self.url,a.a['href']))
                f.write(cap_name+'\n')
                f.write(cap_con+'\n\n')
                print '{0}--{1}->下载完成'.format(book['name'],cap_name)
            f.close()


    def _downCapCon(self,url):
        html = self._getHtml(url)
        html =  html.replace('<br/>','\n')
        html =  html.replace('&nbsp;','')
        soup = BeautifulSoup(html,'lxml')
        con = soup.find('div', id='content').text.replace('chaptererror();','').strip()
        return con

    def _main(self):
        html = self._getHtml(self.url)

        self._parseW(html)

        self._downDetail()

        self._downAllBooks()



if __name__ == '__main__':
    url = 'http://www.qu.la/paihangbang/'
    bo = BiquTest1(url)
    bo._main()
    # print bo.books_1