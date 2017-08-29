# -*- coding: utf-8 -*-
import re
import scrapy
import os
import json
from urllib import parse
from bolezaixian.items import ArticleItemLoader,ZhiHuQuestionItem,ZhiHuAnswerItem

class ZhtSpider(scrapy.Spider):
    name = 'zht'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com']
    img_name = 'captcha.gif'

    custom_settings = {
        'COOKIES_ENABLED':True
    }

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
            'password' :'******',
            'captcha':captcha
        }
        yield scrapy.FormRequest(url=post_url,formdata=post_data,callback=self.post_login)

    def post_login(self,response):
        js_str = json.loads(response.text)
        if 'msg' in js_str and js_str['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True)
        else:
            print('登录失败',js_str)

    def parse(self, response):
        all_urls = response.css('a[href*=question]::attr(href)').extract()
        all_urls = [parse.urljoin(response.url,url) for url in all_urls]
        # all_urls = filter(lambda x:True if x.startswith('https') else False,all_urls)
        for url in all_urls:
            f_res = re.match(r'(.*question/(\d+))($|.*)',url)
            if f_res:
                question_url =f_res.group(1)
                question_id =f_res.group(2)
                yield scrapy.Request(url=question_url,meta={'question_id':question_id},callback=self.parse_question)
                #调试断开
                break


    def parse_question(self,response):
        question_id = response.meta.get('question_id')
        item_loader = ArticleItemLoader(item=ZhiHuQuestionItem(),response=response)
        item_loader.add_value('question_id',question_id)
        item_loader.add_value('question_url',response.url)
        item_loader.add_css('question_title','h1.QuestionHeader-title::text')
        item_loader.add_css('question_topic','a.TopicLink div[id]::text')
        item_loader.add_css('question_content','.QuestionRichText')
        item_loader.add_css('question_pinglun','.QuestionHeader-Comment button::text')
        item_loader.add_css('question_huida','h4.List-headerText span::text')
        item_loader.add_css('question_guanzhu','.NumberBoard-value::text')
        item = item_loader.load_item()
        yield item

        question_api = 'https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0'.format(question_id)

        yield scrapy.Request(question_api,callback=self.parse_answer)

    def parse_answer(self,response):
        json_content = json.loads(response.text)

        for i in json_content['data']:
            item_loader = ArticleItemLoader(item=ZhiHuAnswerItem(),response=response)
            item_loader.add_value('question_id',i['question']['id'])
            item_loader.add_value('created',i['created_time'])
            item_loader.add_value('updated',i['updated_time'])
            item_loader.add_value('crawl',0)
            item_loader.add_value('answer_id',i['id'])
            item_loader.add_value('answer_content',i['content'])
            item_loader.add_value('answer_excerpt',i['excerpt'])
            item_loader.add_value('answer_author_name',i['author']['name'])
            item_loader.add_value('answer_author_id',i['author']['id'])
            item_loader.add_value('answer_pl',i['comment_count'])
            item = item_loader.load_item()
            yield item

        # 调试
        # is_next_page = json_content['paging']['is_end']
        # if not is_next_page:
        #     # 下一页json api answer
        #     next_url = json_content['paging']['next']
        #     yield scrapy.Request(next_url,callback=self.parse_answer)
