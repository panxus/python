# coding=utf-8
import requests
from handledb import exec_sql,insert_manydata
kwargs={'user':'root','passwd':'root','db':'tp_blog','host':'localhost','port':3307, 'charset':'utf8'}

class ParseCar(object):

    def carBrand(self):
        # 车牌
        print 'crawl car brand started...'
        start_url = 'http://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=1'
        cons = requests.get(start_url).text
        con = eval(cons)
        try:
            if con['returncode'] == 0 and con['message'] == '成功':
                last = con['result']['branditems']
                itm = [(l['bfirstletter'],l['id'],l['name']) for l in last]
                data = tuple(itm)
                sql = ('''insert into home_brand (firstletter,brand_id,brand_name) values (%s,%s,%s)''')
                insert_manydata(sql,data,**kwargs)
            else:
                print 'response error'
        except Exception,e:
            print 'field error:',e
        print 'crawl car brand end'
    def carSeries(self):
        # 车系
        pass

    def carType(self):
        # 车型
        pass




if __name__ == '__main__':
    po = ParseCar()
    po.carBrand()