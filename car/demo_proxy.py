import sys
from handledb import exec_sql
import socket
import urllib2

dbapi="MySQLdb"
kwargs={'user':'root','passwd':'root','db':'tp_blog','host':'localhost','port':3307, 'use_unicode':True}

class GetIp(object):
    def __init__(self):
        sql='''SELECT  `IP`,`PORT`,`TYPE` FROM  `erp_ip` WHERE  `SPEED`<5 OR `SPEED` IS NULL'''
        self.result = exec_sql(sql,**kwargs)
    def del_ip(self,record):
        '''delete ip that can not use'''
        sql="delete from erp_ip where IP='%s' and PORT='%s'"%(record[0],record[1])
        print(sql)
        exec_sql(sql,**kwargs)
        print(record ," was deleted.")
    def judge_ip(self,record):
        '''Judge IP can use or not'''
        http_url="http://www.baidu.com/"
        https_url="https://www.alipay.com/"
        proxy_type=record[2].lower()
        url=http_url if  proxy_type== "http" else https_url
        proxy="%s:%s"%(record[0],record[1])
        try:
            req=urllib2.Request(url=url)
            req.set_proxy(proxy,proxy_type)
            response=urllib2.urlopen(req,timeout=10)
        except Exception as e:
            print( "Request Error:",e)
            self.del_ip(record)
            return False
        else:
            code=response.getcode()
            if code>=200 and code<300:
                print('Effective proxy',record)
                return True
            else:
                print('Invalide proxy',record)
                self.del_ip(record)
                return False
        
    def get_ips(self):
        print( "Proxy getip was executed.")
        http=[h[0:2] for h in self.result if h[2] =="HTTP" and self.judge_ip(h)]
        https=[h[0:2] for h in self.result if h[2] =="HTTPS" and self.judge_ip(h)]
        print ("Http: ",len(http),"Https: ",len(https))
        return {"http":http,"https":https}