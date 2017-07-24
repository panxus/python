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

    def getSeriesId(self):
        # 车辆id
        return re.search(r'.*var\s+specIDs\s*=\s*(.*?);',self.js,re.S).group(1)

    def getConfig(self):
        # 车辆配置 词典dict
        return re.search(r'.*var\s+config\s*=\s*(.*?);',self.js,re.S).group(1)

    def getColor(self):
        # 外观颜色
        return re.search(r'.*var\s+color\s*=\s*(.*?);',self.js,re.S).group(1)

    def getInnerColor(self):
        # 内饰颜色
        return re.search(r'.*var\s+innerColor\s*=\s*(.*?);',self.js,re.S).group(1)

    def strChangeDict(self,str):
        # 数据转换
        s = str.replace('null',"'null'")
        return eval(s)

    def getResult(self):
        configStr = self.getConfig()
        configDict = self.strChangeDict(configStr)

        colorStr = self.getColor()
        colorDict = self.strChangeDict(colorStr)

        iColorStr = self.getInnerColor()
        iColorDIct = self.strChangeDict(iColorStr)

        try:
            carSeriesId = self.getSeriesId()
            carTypeName = configDict['result']['paramtypeitems'][0]['paramitems'][0]['valueitems']
            carColor = colorDict['result']['specitems'][0]['coloritems']
            innerColor = iColorDIct['result']['specitems'][0]['coloritems']
        except Exception,e:
            print 'field error:',e
        else:
            self.carSeriesId = carSeriesId
            self.carTypeName = carTypeName
            self.carColor = carColor
            self.carInnerColor = innerColor









if __name__ == '__main__':
    ######### ①. #########
    # javascript = file('test_2.html')
    # jsContent = javascript.read()

    ######### ②. #########
    # url = 'http://car.autohome.com.cn/config/series/923.html'
    url = 'http://car.autohome.com.cn/config/series/3170.html'
    s = requests.get(url)
    con = s.text
    jsContent = Selector(text=con).xpath('/html/body/script[7]').extract()[0]
    print jsContent

    # s = parseStr(jsContent)
    # s.getResult()
    # print s.carSeriesId
    # print s.carTypeName
    # print s.carColor
    # print s.carInnerColor