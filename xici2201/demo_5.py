#coding=utf-8
from handledb import exec_sql
import requests
from multiprocessing.dummy import Pool
import time
DBCONFIG = {'host':'127.0.0.1','user':'root','passwd':'root','port':3307,'charset':'utf8','db':'tp_blog'}

po = Pool(20)

class pv(object):
    def __init__(self):
        self.ip_box = []
        pass

    def _dbHandle(self,ip,type):
        ips = ip.split(':')[1][2:]
        sql = 'update erp_ip set is_use = %s where ip = "%s"' % (type,ips)
        print 'sql :',sql
        exec_sql(sql,**DBCONFIG)

    def _handle(self,proxy):
        if proxy.split(':')[0] == "HTTP":
            proxies = {'http': proxy}
            print('正在测试：{}'.format(proxies))
            try:
                r = requests.get('http://www.jiurong.com', proxies=proxies, timeout=3)
                if r.status_code == 200:
                    print('该代理：{}成功存活'.format(proxy))
                    self._dbHandle(proxy,1)
                    self.ip_box.append(proxy)
            except:
                print('该代理{}失效！'.format(proxies))
                self._dbHandle(proxy,-1)
        else:
            proxies = {'https': proxy}
            print('正在测试：{}'.format(proxies))
            try:
                r = requests.get('https://www.baidu.com', proxies=proxies, timeout=3)
                if r.status_code == 200:
                    print('该代理：{}成功存活'.format(proxy))
                    self._dbHandle(proxy,1)
                    self.ip_box.append(proxy)
            except:
                print('该代理{}失效！'.format(proxies))
                self._dbHandle(proxy,-1)


    def _main(self):
        sql = 'select ip,port,type from erp_ip where is_use = 2 order by id desc limit 1000'
        res = exec_sql(sql,**DBCONFIG)
        if res:
            rs = [i[2]+'://'+i[0]+':'+i[1] for i in res]
            po.map(self._handle,rs)


if __name__ == '__main__':
    start = time.time()
    s = pv()
    s._main()
    end = time.time()
    print s.ip_box
    print end-start