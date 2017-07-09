#coding=utf-8
from bs4 import BeautifulSoup
import requests
import re
import threading


def searchThings(url):
    print 'threading started at %s ' % threading.current_thread()
    head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    s = requests.get(url=url,headers=head).content
    soup = BeautifulSoup(s,'lxml')
    art= soup.find_all('article',class_='thing')
    for i in art:
        print i.find('a',title=re.compile('.+')).string

    print 'threading ended at %s ' % threading.current_thread()
    print '----------------------------------------------------------'


sem = threading.Semaphore(2)

def threadingSearch(sem,url):
    sem.acquire()
    searchThings(url)
    sem.release()

def down_store(start,end):
    old_url = 'https://knewone.com/discover?page=1'
    for i in range(start,end+1):
        if i==1:
            url = old_url
        else:
            url = old_url + '&page='+str(i)
        # searchThings(url)
        # threading.Thread(target=searchThings,args=[url]).start()
        threading.Thread(target=threadingSearch,args=[sem,url]).start()

if __name__ == '__main__':
    down_store(1,3)