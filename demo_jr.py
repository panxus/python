#coding=utf-8
from bs4 import BeautifulSoup
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def trim_lr(str):
    return re.sub('\s+','',str)

def get_id(str):
    return re.search(r'\d+',str).group()

def printLoan(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Referer':'https://www.jiurong.com/user/vip.html'}
    con = requests.get(url,headers=headers).content
    soup = BeautifulSoup(con,'lxml')
    slist = soup.find_all('div',class_='sList')
    loan_list = []
    for i in slist:
        flag = {}
        loan_a = i.find('a',class_='orgban')
        href = loan_a.attrs['href']
        flag['href'] = 'https://www.jiurong.com' + href
        flag['id'] = get_id(href)
        flag['loan_title'] = loan_a.attrs['href']
        loan_span = i.find('span',class_='rate font-warning')
        # print trim_lr(loan_span.contents[0])
        # print loan_span.contents[1].i.string
        flag['apr'] = trim_lr(loan_span.contents[0])
        flag['dealline'] = i.find('span',class_='period').string
        flag['money'] = i.find('span',class_='money font-warning').string
        flag['repay_method'] = i.find('span',class_='mode').string
        flag['process'] = i.find('label',class_='per').string
        loan_list.append(flag)

    return loan_list

if __name__ == '__main__':
    p = input('输入页数:')

    for i in range(p):
        index = i+1
        url = 'http://www.jiurong.com/loan/index/p/'+str(index)
        loan_list = printLoan(url)
        print '第{0}页 begin ---------------'.format(index)
        for i in loan_list:
            print '标id:%(id)s---,链接:%(href)s,---标:%(loan_title)s---,周期:%(dealline)s---,利率:%(apr)s---,金额:%(money)s---,还款方式:%(repay_method)s---,投标进度:%(process)s' % i
        print '第{0}页 end ---------------'.format(index)