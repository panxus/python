#coding=utf-8
import requests
import urlparse
import os
import random
import urllib
from bs4 import BeautifulSoup
class ParseWeb(object):
    def __init__(self,url):
        self.url = url
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        self.box = ''
        # 1.验证url
        code,html = self._verify()
        if code:
            self.box = html
            # 2.建立目录
            dirc = self._makeDir()
            # 3.解析页面
            if dirc:
                self._parse(dirc)
        else:
            print '页面解析失败'


    def _makeDir(self):
        urlSe = urlparse.urlparse(self.url)
        dir_f = urlSe.netloc+'_1'
        flag = True
        while flag and os.path.isdir(dir_f):
            rand = random.randint(1,100)
            new_d = dir_f+'_'+str(rand)
            if not os.path.isdir(new_d):
                dir_f = new_d
                flag = False
        os.mkdir(dir_f)
        if os.path.isdir(dir_f):
            os.mkdir(dir_f+'/'+'js')
            os.mkdir(dir_f+'/'+'css')
            os.mkdir(dir_f+'/'+'images')
            return dir_f
        return None

    def _parse(self,dirc):
        con = requests.get(self.url,headers=self.headers).content
        soup = BeautifulSoup(con,'lxml')
        links = soup.find_all('link')
        for link in links:
            if link['href']:
                self._downResource(link['href'],dirc)
        srcs = soup.select('script[src]')
        for src in srcs:
            if src['src']:
                self._downResource(src['src'],dirc)
        imgs = soup.find_all('img')
        for img in imgs:
            if img['src']:
                self._downResource(img['src'],dirc)
        with open(dirc+'/index.html','wb+') as f:
            f.write(self.box)
            f.close()


    def _downResource(self,url,dirc):
        url = self._purl(url)
        old_url = urlparse.urljoin(start_url,url)
        diro = self._getDirByUrl(url)
        fname = url.split('/')[-1]
        real_dir = dirc+'/'+diro+'/'+fname
        sreq = requests.get(old_url)
        try:
            if sreq.status_code == 200:
                with open(real_dir,'wb') as f:
                    f.write(sreq.content)
                    f.close()
                print '文件 %s 下载到 %s 成功.' % (old_url,real_dir)
                newUrl = './'+diro+'/'+fname
                self.box = self.box.replace(url,newUrl)
            else:
                print '文件 %s 下载到 %s 失败.' % (old_url,real_dir)

        except Exception,e:
            print e


    def _purl(self,url):
        if '?' in url:
            return url.split('?')[0]
        else:
            return url

    def _getDirByUrl(self,url):
        ext = url.split('.')[-1]
        if ext == 'css':
            return 'css'
        elif ext == 'js':
            return 'js'
        else:
            return 'images'
    def _verify(self):
        con = requests.get(self.url,self.headers)
        if con.status_code == 200:
            return True,con.content
        else:
            return False,con.content

if __name__ == '__main__':
    start_url = 'http://www.coladesign.cn/'
    pObj = ParseWeb(start_url)

