from handledb import exec_sql
import requests
import urllib2

db = {'host':'127.0.0.1','port':3307,'db':'tp_blog','user':'root','passwd':'root','charset':'utf8'}


class VerifyProxy(object):
    def __init__(self):
        sql = ''' select ip,port,type from erp_ip where is_use = 0 limit 50'''
        self.result = exec_sql(sql,**db)

    def deleteIp(self,ip):
        print 'ready delete ip : %s' % ip
        sql = '''delete from erp_ip where ip = "%s"''' % ip
        exec_sql(sql,**db)
        pass

    def parseHttp(self,data):
        # print data
        url = 'http://www.baidu.com'
        req = urllib2.Request(url=url)
        host = '%s:%s' % (data[0],data[1])
        type_ = data[2]
        req.set_proxy(host=host,type=type_)
        try:
            s = urllib2.urlopen(req)
        except Exception,e:
            self.deleteIp(data[0])
            print 'request error :',e
        else:
            if s.getcode >=200 and s.getcode < 300:
                print 'success : %s' % data[0]
            else:
                self.deleteIp(data[0])
                print 'failed : %s' % data[0]

    def doThis(self):

        http = [i[0:2] for i in self.result if i[2]=='HTTP' and self.parseHttp(i)]
        https = [i[0:2] for i in self.result if i[2]=='HTTPS' and self.parseHttp(i)]

        print http
        print https
        return self.result







if __name__ == '__main__':
    s = VerifyProxy()
    print s.doThis()