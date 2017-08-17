# -*- coding: utf-8 -*-
import scrapy
import json
import os
class ZhSpider(scrapy.Spider):
    name = 'zh'
    # allowed_domains = ['www.zhihu.com/']
    start_urls = ['https://www.zhihu.com/']
    headers = {
        'Host':'www.zhihu.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Referer':'https://www.zhihu.com/',
    }
    def start_requests(self):

        yield scrapy.Request(url='https://www.zhihu.com/captcha.gif?type=login',callback=self.getCaptcha,headers=self.headers)

    def getCaptcha(self,response):
        with open('code.gif','wb') as f:
            f.write(response.body)
            f.close()
        os.startfile('code.gif')
        captcha = input('输入验证码:\n')
        yield scrapy.Request(url='https://www.zhihu.com/#signin',callback=self.parse_index,headers=self.headers,meta={'captcha':captcha})
    def parse_index(self,response):
        captcha = response.meta.get('captcha')
        csrf = response.xpath('//input[@name="_xsrf"]/@value').extract_first()
        if csrf:
            post_data = {
                'phone_num':'17607188711',
                '_xsrf' : csrf,
                'password' :'****',
                'captcha':captcha
            }
            yield scrapy.FormRequest(url='https://www.zhihu.com/login/phone_num',formdata=post_data,headers=self.headers,callback=self.handle_result)
        else:
            print('csrf error?')

    def handle_result(self,response):
        js = json.loads(response.body)
        if 'msg' in js and js['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True,headers=self.headers)
        else:
            print(js)


    def parse(self, response):
        #the last
        pass
