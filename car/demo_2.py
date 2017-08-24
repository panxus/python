#coding=utf-8
# 解析汽车之家 参数配置 页面
import re
import requests
from scrapy.selector import Selector

class parseStr(object):
    def __init__(self,js):
        self.js = js
        self.carSeriesId = []
        self.carTypeName = []
        self.carColor = []
        self.carInnerColor = []
        self.carZhiDaoPrice = []
        self.carcityTime = []

    def getSetting(self):
        # 车辆id  词典dict
        seriesIds = re.search(r'.*var\s+specIDs\s*=\s*(.*?);',self.js,re.S).group(1)
        # 车辆配置
        configs = re.search(r'.*var\s+config\s*=\s*(.*?);',self.js,re.S).group(1)
        # 外观颜色
        colors = re.search(r'.*var\s+color\s*=\s*(.*?);',self.js,re.S).group(1)
        # 内饰颜色
        innerColor = re.search(r'.*var\s+innerColor\s*=\s*(.*?);',self.js,re.S).group(1)

        return seriesIds,configs,colors,innerColor

    def strChangeDict(self,str):
        # 数据转换
        s = str.replace('null',"'null'")
        return eval(s)


    def getResult(self):
        try:
            carSeriesId,configStr,colorStr,iColorStr= self.getSetting()
            configDict = self.strChangeDict(configStr)
            colorDict = self.strChangeDict(colorStr)
            iColorDIct = self.strChangeDict(iColorStr)
            #车系名称
            carTypeName = configDict['result']['paramtypeitems'][0]['paramitems'][0]['valueitems']
            #指导价
            zhiDaoPrice = configDict['result']['paramtypeitems'][0]['paramitems'][1]['valueitems']
            # 上市时间
            cityTime = configDict['result']['paramtypeitems'][0]['paramitems'][4]['valueitems']
            # 外观颜色
            carColor = colorDict['result']['specitems'][0]['coloritems']
            # 内饰颜色
            innerColor = iColorDIct['result']['specitems']
        except Exception as e:
            print('field error:',e)
        else:
            self.carSeriesId = carSeriesId
            self.carTypeName = carTypeName
            self.carColor = carColor
            self.carInnerColor = innerColor
            self.carZhiDaoPrice = zhiDaoPrice
            self.carcityTime = cityTime









if __name__ == '__main__':
    ######### ①. #########
    javascript = open('test_1.html')
    jsContent = javascript.read()

    ######### ②. #########
    # url = 'http://car.autohome.com.cn/config/series/923.html'
    # url = 'http://car.autohome.com.cn/config/series/650.html'
    # s = requests.get(url)
    # con = s.text
    # jsContent = Selector(text=con).xpath('/html/body/script[7]').extract()[0]
    # print jsContent

    s = parseStr(jsContent)
    s.getResult()
    print(s.carSeriesId)
    print(s.carTypeName)
    print(s.carColor)
    print(s.carInnerColor)
    print(s.carZhiDaoPrice)
    print(s.carcityTime)