#coding=utf-8
import requests
from urllib import parse
import os
import random
import re
from bs4 import BeautifulSoup
import codecs
class ParseWeb(object):
    def __init__(self,url):
        # self.rcompile = re.compile(r'url.*?\'(.*?fonts.*?)\'.*?\)')
        self.rcompile = re.compile(r'url\(("|\')?(.*?fonts.*?)("|\')?\)')
        self.scompile = re.compile(r'("//hm.baidu.com.*?)"')
        self.url = url
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        self.box = ''
        # 1.验证url
        code,html = self._verify()
        if code:
            self.box = html.decode('utf-8')
            # 2.建立目录
            dirc = self._makeDir()
            # 3.解析页面
            if dirc:
                self._parse(dirc)
        else:
            print('页面解析失败')


    def _makeDir(self):
        urlSe = parse.urlparse(self.url)
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
            os.mkdir(dir_f+'/'+'fonts')
            return dir_f
        return None

    def _judgeHref(self,href):
        # 排除 异常地址
        ext = href.split('.')[-1]
        if ext in ['com','cn','org'] or href[-1] == '/' or href == '':
            return False
        else:
            return True

    def _parse(self,dirc):
        con = requests.get(self.url,headers=self.headers).content
        soup = BeautifulSoup(con,'lxml')

        links = soup.find_all('link')
        hr = [link['href'] for link in links if self._judgeHref(link['href'])]
        for hi in hr:
            self._downResource(hi,dirc)
            if self._isCss(hi):
                #解析css样式里可能存在的字体样式
                hi =  parse.urljoin(self.url,hi)
                s = requests.get(hi).content.decode('utf-8')
                index1 = hi.rfind('/')
                hi = hi[:index1]
                index2 = hi.rfind('/')
                first_url = hi[:index2]
                for i in self.rcompile.findall(s):
                    la_url = first_url + i[1][2:]
                    self._downResource(la_url,dirc)

        srcs = soup.select('script[src]')
        for src in srcs:
            self._downResource(src['src'],dirc)

        imgs = soup.select('img[src]')
        for img in imgs:
            self._downResource(img['src'],dirc)


        #替换百度统计
        self.box = self.scompile.sub('""',self.box)

        try:
            with open(dirc+'/index.html','wb+') as f:
                f.write(self.box.encode('utf-8'))
            f.close()
        except Exception as e:
            print('页面写入失败',e)

    # 下载资源
    # url 资源
    # dirc 主文件夹名
    def _downResource(self,url,dirc):
        url = self._purl(url)
        old_url = parse.urljoin(self.url,url)
        diro = self._getDirByUrl(url)
        fname = url.split('/')[-1]
        real_dir = dirc+'/'+diro+'/'+fname
        sreq = requests.get(old_url)
        try:
            if sreq.status_code == 200:
                with codecs.open(real_dir,'wb') as f:
                    f.write(sreq.content)
                    f.close()
                print('文件 %s 下载到 %s 成功.' % (old_url,real_dir))
                newUrl = './'+diro+'/'+fname
                self.box = self.box.replace(url,newUrl)
            else:
                print('文件 %s 下载到 %s 失败.' % (old_url,real_dir))
        except Exception as e:
            print(e)


    def _purl(self,url):
        # 文件全路径 去除版本号
        if '?' in url:
            return url.split('?')[0]
        else:
            return url

    def _isCss(self,url):
        #
        if '?' in url:
            url = url.split('?')[0]
        if url.split('.')[-1] == 'css':
            return True
        else:
            return False

    def _getDirByUrl(self,url):
        # 获取文件目录
        ext = url.split('.')[-1]
        if ext == 'css':
            return 'css'
        elif ext == 'js':
            return 'js'
        elif ext in ['jpg','gif','png','jpeg','ico']:
            return 'images'
        else:
            return 'fonts'

    def _verify(self):
        # 验证目录
        con = requests.get(self.url,self.headers,timeout=20)
        if con.status_code == 200:
            return True,con.content
        else:
            return False,con.content

if __name__ == '__main__':
    start_url = 'http://coladesign.cn/'
    pObj = ParseWeb(start_url)

