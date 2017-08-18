import requests
import re
import re
import codecs
from scrapy.selector import Selector
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
           'Cookie':'d_c0="AEACdhmcvQuPThvvr7DyU7jRbnBNYb32y9E=|1494483056"; _zap=3becb3f9-9f8c-4cd5-b0e3-633e760a0208; q_c1=521d7a920b5b4caea28fa26d40ba56bf|1499738596000|1493257457000; OUTFOX_SEARCH_USER_ID_NCOO=1686118557.9132056; capsion_ticket="2|1:0|10:1501559156|14:capsion_ticket|44:MmE2YmE1YzU1OTM5NGJmY2ExOWUxODUzMDI1YjhhNDE=|56135edf073fde7d77166d094440a42e11e8b56243f20282a829b5177ef65b4e"; q_c1=521d7a920b5b4caea28fa26d40ba56bf|1502415742000|1493257457000; r_cap_id="YmI1YzljYTRhZDIwNDQ5Nzg0ZDg4OTRlNTBlZjJkZTY=|1502961711|4790de1f0c2955146831990008e8c455fea53544"; cap_id="OGJjOWU4YTVmYjlhNDVhY2I3ZWQyYTI4YzM0OGZiZWI=|1502961711|3397e9b4290acbe03499b3488efdd0c9fd90111c"; z_c0=Mi4xeGFSbEFnQUFBQUFBUUFKMkdaeTlDeGNBQUFCaEFsVk5QTzI4V1FCSVAtZUhWMVBPblg3bHpmR2pVVHJDZmRRQ0pn|1502961724|ff440b5f7c00d1a050a0d9a77ee1f2740a443f35; __utma=51854390.480952644.1502954425.1502961701.1503033635.3; __utmz=51854390.1503033635.3.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/panxu94/activities; __utmv=51854390.100-1|2=registration_date=20151220=1^3=entry_date=20151220=1; aliyungf_tc=AQAAAJKBV0rCsQIAqrhidwl2gukqIHZm; l_cap_id="ZjY4MDA1ZmY0YTc1NGMwOGE1MGE3ODRmMWU4MzAxOWI=|1503038751|fba1caaa3e8038c3bc0879941894ef8e1fd5954a"; _xsrf=044bc131-6934-47ce-aacd-ea97d65eac90'}
# s = requests.get('https://www.zhihu.com/',headers=headers)
# print(s.content)
# with codecs.open('ind.html','wb') as f:
#     f.write(s.content)
#     f.close()


con = codecs.open('ind.html','r','utf-8').read()
# print(con.read())
# /question/48509984
# https://www.zhihu.com/question/33593693/answer/215963458"
# https://www.zhihu.com/question/33593693/answer/215963458"
# /question/33593693/answer/215963458


s = Selector(text=con).css('a[href*=question]::attr(href)').extract()
# print(s)

# s = re.findall(r'.*href="(.*question)"',con,re.DOTALL)
# if s:
#     print(s.group(1))
#     print('--')

# print(s)
from urllib import parse

# sl = ['https://www.zhihu.com/question/33593694/answer/215963458','https://www.zhihu.com/question/33593693','/question/33593693/question','javascript']
pr = 'https://www.zhihu.com'
ss = [parse.urljoin(pr,i) for i in s]

# s = filter(lambda x:True if x else False,sl)


#
for i in ss:
    ss2 = re.match(r'(.*question/(\d+))($|.*)',i)
    if ss2:
        qs_url = ss2.group(1)
        qs_id = ss2.group(2)
        s = requests.get(url=qs_url,headers=headers)
        question_title=Selector(text=s.content).css('h1.QuestionHeader-title::text').extract()
        question_topic=Selector(text=s.content).css('a.TopicLink div[id]::text').extract()
        question_content=Selector(text=s.content).css('.QuestionRichText').extract()
        question_pinglun=Selector(text=s.content).css('.QuestionHeader-Comment button::text').extract()
        question_huida=Selector(text=s.content).css('h4.List-headerText span::text').extract()
        question_guanzhu=Selector(text=s.content).css('.NumberBoard-value::text').extract()
        question_liulan=Selector(text=s.content).css('.NumberBoard-value::text').extract()
        pass
