#coding=utf-8
import requests
import re
from HTMLParser import HTMLParser
def _attr(name,list):
    for i in list:
        if i[0] == name:
            return i[1]
    return None
class ParsePoem(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.ci = []
        self.flag = {}
        self.inDiv = False
        self.inSpan = False
        self.inA = False
        self.authorPattern = re.compile(r'\(.*\)',re.VERBOSE)

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and _attr('class',attrs) == 'typecont':
            self.inDiv = True
        if self.inDiv and tag == 'span':
            self.inSpan = True
        if self.inDiv and tag == 'a':
            self.flag['url'] = _attr('href',attrs)
            self.inA = True
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
            self.ci.append(self.flag)
            self.flag = {}


if __name__ == '__main__':
    # fl = file('test.html')
    # cont = fl.read()
    cont = requests.get('http://so.gushiwen.org/gushi/songsan.aspx').content
    # print cont
    pob = ParsePoem()
    pob.feed(cont)
    last = pob.ci
    # print last
    for i in last:
        print '%(author)s - %(title)s - %(url)s' % i
        # print i
