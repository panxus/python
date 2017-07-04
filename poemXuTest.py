#coding=utf-8
import requests
import re
from HTMLParser import HTMLParser
def _attr(name,list):
    for i in list:
        if i[0] == name:
            return i[1]
    return None
def trim_ws(str):
    s = re.sub('\s*','',str)
    return s
def trim_br(str):
    return re.sub('<br/>|<br>|<br />','',str)
    # return str.replace('<br/>|<br>|<br />','')

def periodTrans(str):
    return str.replace('。','。\n')

class ParsePoem(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.poem = []
        self.flag = {}
        self.inDiv = False
        self.inSpan = False
        self.inA = False
        self.authorPattern = re.compile(r'\(.*?\)',re.VERBOSE)

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and _attr('class',attrs) == 'typecont':
            self.inDiv = True
        if self.inDiv and tag == 'span':
            self.inSpan = True
        if self.inDiv and tag == 'a':
            self.inA = True
            self.flag['url'] = _attr('href',attrs)


    def handle_endtag(self, tag):
        if tag == 'span':
            self.inSpan = False
        if tag == 'a':
            self.inA = False

    def handle_data(self, data):
        if self.inA:
            self.flag['title'] = data
        if self.inSpan and self.authorPattern.match(data):
            self.flag['author'] = data
            self.poem.append(self.flag)
            self.flag = {}

class ParsePoemContent(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.poemC = []
        self.poemF = {}
        self.InDiv = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and _attr('class',attrs) == 'contson':
            self.InDiv = True
            self.poemF['id'] = _attr('id',attrs)

    def handle_endtag(self, tag):
        if tag == 'div':
            self.InDiv = False

    def handle_data(self, data):
        if self.InDiv:
            self.poemF['content'] = data
            self.poemC.append(self.poemF)
            self.poemF = {}


def downPoem(url):
    newUrl  = 'http://so.gushiwen.org'+url
    con     = requests.get(newUrl).content
    s    = ParsePoemContent()
    real_con = trim_br(con)
    s.feed(real_con)
    for i in s.poemC:
        if re.search('\d+',i['id']).group() == re.search('\d+',url).group():
            # return i['content']
            return periodTrans(i['content'])

if __name__ == '__main__':
    # fl = file('test.html')
    # cont = fl.read()
    cont = requests.get('http://so.gushiwen.org/gushi/tangshi.aspx').content
    pob = ParsePoem()
    pob.feed(cont)
    last = pob.poem
    s  = file('poem.txt','wb')
    start = '唐诗三百首 : 共 '+ str(len(last))+' 首：\n\n'
    s.write(start)
    flag = 1
    for i in pob.poem:
        con = '\n%(title)s\n--%(author)s\n--%(url)s\n' % i
        s.write(con)
        print 'downing '+str(flag)+'---- '+ i['url']
        pcon = downPoem(i['url'])
        # print pcon
        s.write(pcon)
        flag+=1
