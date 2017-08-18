# -*- coding: utf-8 -*-
import re
import scrapy
import os
import json
from urllib import parse
from bolezaixian.items import ZhiHuQuestionItem,ArticleItemLoader

class ZhtSpider(scrapy.Spider):
    name = 'zht'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com']
    img_name = 'captcha.gif'

    def start_requests(self):
        yield scrapy.Request('https://www.zhihu.com/#signin',callback=self.get_xsrf)

    def get_xsrf(self,response):
        xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract()[0]
        if xsrf:
            img_url = 'https://www.zhihu.com/captcha.gif?type=login'
            yield scrapy.Request(img_url,callback=self.get_captcha,meta={'xsrf':xsrf})

    def get_captcha(self,response):
        with open(self.img_name,'wb') as f:
            f.write(response.body)
            f.close()
        os.startfile(self.img_name)
        captcha = input('输入验证码:\n>')
        xsrf = response.meta.get('xsrf')
        post_url = 'https://www.zhihu.com/login/phone_num'
        post_data = {
            'phone_num':'17607188711',
            '_xsrf' : xsrf,
            'password' :'****',
            'captcha':captcha
        }
        yield scrapy.FormRequest(url=post_url,formdata=post_data,callback=self.post_login)

    def post_login(self,response):
        js_str = json.loads(response.text)
        if 'msg' in js_str and js_str['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True)
        else:
            print('登录失败')

    def parse(self, response):
        all_urls = response.css('a[href*=question]::attr(href)').extract()
        all_urls = [parse.urljoin(response.url,url) for url in all_urls]
        # all_urls = filter(lambda x:True if x.startswith('https') else False,all_urls)
        for url in all_urls:
            f_res = re.match(r'(.*question/(\d+))($|.*)',url)
            if f_res:
                question_url =f_res.group(1)
                question_id =f_res.group(2)
                scrapy.Request(url=question_url,meta={'question_id':question_id},callback=self.parse_question)
                #调试
                break


    def parse_question(self,response):

        item_loader = ArticleItemLoader(item=ZhiHuQuestionItem(),response=response)
        item_loader.add_value('question_id',response.meta.get('question_id'))
        item_loader.add_value('question_url',response.url)
        item_loader.add_css('question_title','h1.QuestionHeader-title::text')
        item_loader.add_css('question_topic','a.TopicLink div[id]::text')
        item_loader.add_css('question_content','.QuestionRichText')
        item_loader.add_css('question_pinglun','.QuestionHeader-Comment button::text')
        item_loader.add_css('question_huida','h4.List-headerText span::text')
        item_loader.add_css('question_guanzhu','.NumberBoard-value::text')
        item = item_loader.load_item()
        yield item

