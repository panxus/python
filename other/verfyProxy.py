from handledb import exec_sql
import requests
import urllib2

db = {'host':'127.0.0.1','port':3307,'db':'tp_blog','user':'root','passwd':'root','charset':'utf8'}


class VerifyProxy(object):
    def __init__(self):
        sql = ''' select ip,port,type from erp_ip where is_use = 0 limit 50'''
        self.result = exec_sql(sql,**db)
    def doThis(self):
        return self.result







if __name__ == '__main__':
    s = VerifyProxy()
    print s.doThis()