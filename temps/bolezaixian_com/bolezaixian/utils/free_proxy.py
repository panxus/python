# -*- coding: utf-8 -*-
# 免费代理抓取
import requests
from scrapy.selector import Selector
from handledb import insert_manydata
from datetime import datetime
import time
import re
kwargs={'user':'root','passwd':'','db':'tp_blog','host':'localhost','port':3306, 'charset':'utf8'}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

class XiCi(object):
    def __init__(self,start_page,end_page):
        self.start_page = start_page
        self.end_page = end_page
        self.base_url = 'http://www.xicidaili.com/nn/%d'
        self.box_1 = []

    def start_crawl(self):
        for i in range(self.start_page,self.end_page+1):
            # print(i)
            self.crawl(self.base_url % int(i))

    def crawl(self,url):
        req = requests.get(url,headers=headers,timeout=5)
        if req.status_code == 200:
            trs = Selector(text=req.text).xpath('//*[@id="ip_list"]/tr[position()>1]')
            for tr in trs:
                ip = tr.xpath('td[2]/text()').extract()[0]
                port = tr.xpath('td[3]/text()').extract()[0]
                type = tr.xpath('td[6]/text()').extract()[0]
                crawl_time = datetime.now()
                self.box_1.append((ip,port,type,crawl_time))

    def save_ip(self):
        if self.box_1:
            tData = tuple(self.box_1)
            tSql = ''' insert into erp_ip (ip,port,type,crawl_time,ver_time,is_use,source) values (%s,%s,%s,%s,0,0,1)'''
            insert_manydata(tSql,tData,**kwargs)

class Kuaidl(object):
    def __init__(self,start_page,end_page):
        self.start_page = start_page
        self.end_page = end_page
        self.base_url = 'http://www.kuaidaili.com/free/inha/%d/'
        self.box_2 = []
    def start_crawl(self):
        for i in range(self.start_page,self.end_page+1):
            self.crawl(self.base_url % int(i))
            time.sleep(1)

    def crawl(self,url):
        req = requests.get(url,headers=headers,timeout=5)
        if req.status_code == 200:
            trs = Selector(text=req.text).xpath('//*[@id="list"]/table/tbody/tr')
            for tr in trs:
                ip = tr.xpath('td[1]/text()').extract()[0]
                port = tr.xpath('td[2]/text()').extract()[0]
                type = tr.xpath('td[4]/text()').extract()[0]
                crawl_time = datetime.now()
                self.box_2.append((ip,port,type,crawl_time))


    def save_ip(self):
        if self.box_2:
            tData = tuple(self.box_2)
            tSql = ''' insert into erp_ip (ip,port,type,crawl_time,ver_time,is_use,source) values (%s,%s,%s,%s,0,0,2)'''
            insert_manydata(tSql,tData,**kwargs)

class Ip66(object):
    def __init__(self,getnum,proxytype):
        self.getnum = getnum
        self.proxytype = proxytype
        self.base_url = 'http://www.xicidaili.com/nn/%d'
        self.box_1 = []

    def _main(self):
        url = 'http://www.66ip.cn/nmtq.php?getnum={0}&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype={1}&api=66ip'.format(self.getnum, self.proxytype)
        s = requests.get(url,headers=headers)
        if s.status_code == 200:
            html = s.text
            li = re.findall('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{2,5}',html,re.S)
            type_ = 'HTTP' if proxytype == 0 else 'HTTPS'
            crawl_time = datetime.now()
            la = ((i.split(':')[0],i.split(':')[1],type_,crawl_time) for i in li)
            sql = '''insert into erp_ip (ip,port,type,crawl_time,ver_time,is_use,source) values (%s,%s,%s,%s,0,0,3)'''
            data = tuple(la)
            insert_manydata(sql,data,**kwargs)
        else:
            print('request error')

if __name__ == '__main__':

    ##### 1.西刺 #####

    # xc = XiCi(1,3)
    # xc.start_crawl()
    # xc.save_ip()

    ##### 2.快代理 #####

    # xc = Kuaidl(1,2)
    # xc.start_crawl()
    # xc.save_ip()

    ##### 3.66ip #####

    #最多800
    # 0 http  1 https 2全部
    # getnum = 300
    # proxytype = 0
    # xc = Ip66(getnum,proxytype)
    # xc._main()

    pass




