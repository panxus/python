#coding=utf-8
#抓取 66ip 免费高匿代理
# 2017年8月10
import requests
from handledb import insert_manydata
import re
kwargs={'user':'root','passwd':'root','db':'tp_blog','host':'localhost','port':3307, 'charset':'utf8'}

def _main(getnum,proxytype):
    url = 'http://www.66ip.cn/nmtq.php?getnum={0}&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype={1}&api=66ip'.format(getnum,proxytype)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    s = requests.get(url,headers=headers)
    html = s.content
    li = re.findall('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{2,5}',html,re.S)
    if proxytype == 0:
        type_ = 'HTTP'
    else:
        type_ = 'HTTPS'
    la = ((i.split(':')[0],i.split(':')[1],'','',type_,'','','','',0,3) for i in li)
    sql = '''insert into erp_ip (ip,port,address,niming,type,speed,link_time,live_time,ver_time,is_use,source) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    data = tuple(la)
    insert_manydata(sql,data,**kwargs)


if __name__ == '__main__':
    #最多800
    getnum = 300
    # 0 http  1 https 2全部
    proxytype = 1
    _main(getnum,proxytype)