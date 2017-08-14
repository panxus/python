#coding=utf-8
from selenium import webdriver



class Kdl(object):
    def __init__(self,s,e):
        self.url = []
        self.data =[]
        self.fileName = 'port_2.txt'

        self.getUrl(s,e)
        self.getItem()
        self.downData()

    def getUrl(self,s,e):
        s_url = 'http://www.kuaidaili.com/free/inha/%d/'
        for i in xrange(s,e+1):
            self.url.append(s_url % i)

    def getItem(self):
        if self.url:
            driver = webdriver.PhantomJS('D:/phantomjs/phantomjs-2.1.1-windows/bin/phantomjs.exe')
            for url in self.url:
                driver.get(url)
                driver.implicitly_wait(3)
                trs = driver.find_elements_by_xpath('//*[@id="list"]/table/tbody/tr')
                for tr in trs:
                    item = {}
                    item['ip'] = tr.find_element_by_xpath('td[1]').text
                    item['port'] = tr.find_element_by_xpath('td[2]').text
                    item['type'] = tr.find_element_by_xpath('td[4]').text
                    self.data.append(item)
            driver.quit()


    def downData(self):
        if self.data:
            with open(self.fileName,'a+') as f:
                for data in self.data:
                    f.write('type:'+data['type']+',ip:'+data['ip']+',port:'+data['port']+'\n')
                f.close()


if __name__ == '__main__':
    s = Kdl(1,3)
    print s.data