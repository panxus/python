# coding=utf-8
# 2w+车型号 抓取时间过长
import requests
from handledb import exec_sql,insert_manydata
kwargs={'user':'root','passwd':'root','db':'tp_blog','host':'localhost','port':3307, 'charset':'utf8'}

class ParseCar(object):

    def carBrand(self):
        # 车牌
        print 'crawl car brand start...'
        start_url = 'http://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=1'
        cons = requests.get(start_url).text
        con = eval(cons)
        try:
            if con['returncode'] == 0 and con['message'] == '成功':
                last = con['result']['branditems']
                # itm = [(l['bfirstletter'],l['id'],l['name']) for l in last]
                # data = tuple(itm)
                # sql = ('''insert into home_brand (firstletter,brand_id,brand_name) values (%s,%s,%s)''')
                # insert_manydata(sql,data,**kwargs)
                print 'crawl car brand end'
                print 'crawl car seried start...'
                url = 'http://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=3&value=%d'
                url_2 = 'http://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=5&value=%d'
                for i in last:
                    brand_id = i['id']
                    n_url = url % brand_id
                    con = requests.get(n_url).text
                    cons = eval(con)
                    if cons['message'] == '成功' and cons['returncode'] == 0:
                        seriesDIct = []
                        for dv in cons['result']['factoryitems']:
                            print 'start crawl car brand : %s' % i['name']
                            factory_id = dv['id']
                            factory_name = dv['name']
                            for la in dv['seriesitems']:
                                seriesFlag = {}
                                seriesFlag['brand_id'] = brand_id
                                seriesFlag['factory_id'] = factory_id
                                seriesFlag['factory_name'] = factory_name
                                seriesFlag['series_id'] = la['id']
                                seriesFlag['series_name'] = la['name']
                                seriesFlag['series_order'] = la['seriesorder']
                                seriesDIct.append(seriesFlag)
                        # la = [(a['brand_id'],a['series_id'],a['series_name'],a['series_order'],a['factory_id'],a['factory_name']) for a in seriesDIct]
                        # data = tuple(la)
                        # sql = '''insert into home_series (brand_id,series_id,series_name,series_order,factory_id,factory_name) values (%s,%s,%s,%s,%s,%s)'''
                        # insert_manydata(sql,data,**kwargs)
                                murl = url_2 % la['id']
                                lCon = requests.get(murl).text
                                lon = eval(lCon)
                                if lon['message']== '成功' and lon['returncode'] == 0:
                                    typeDict = []
                                    for dl in lon['result']['yearitems']:
                                        typeFlag = {}
                                        for dla in dl['specitems']:
                                            typeFlag['series_id'] = la['id']
                                            typeFlag['years_id'] = dl['id']
                                            typeFlag['years_name'] = dl['name']

                                            typeFlag['type_id'] = dla['id']
                                            typeFlag['type_name'] = dla['name']
                                            typeFlag['maxprice'] = dla['maxprice']
                                            typeFlag['minprice'] = dla['minprice']
                                            typeFlag['state'] = dla['state']
                                            typeDict.append(typeFlag)
                                    typeTup = [(b['type_id'],b['type_name'],b['maxprice'],b['minprice'],b['state'],b['years_name'],b['years_id'],b['series_id']) for b in typeDict]
                                    tData = tuple(typeTup)
                                    tSql = ''' insert into home_detail (type_id,type_name,maxprice,minprice,state,years_name,years_id,series_id) values (%s,%s,%s,%s,%s,%s,%s,%s)'''
                                    insert_manydata(tSql,tData,**kwargs)

                print 'crawl car seried end...'
        except Exception,e:
            print 'field error:',e


if __name__ == '__main__':
    po = ParseCar()
    po.carBrand()