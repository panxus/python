from HTMLParser import HTMLParser
import re
import requests

class getAuthor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.poem = []
        self.flag = {}
        self.inDiv = False
        self.inA = False
        self.inSpan = False
        self.partten = re.compile(r'\(.+\)',re.VERBOSE)

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and _attr('class',attrs) == 'typecont':
            self.inDiv = True
        if self.inDiv and tag == 'a':
            self.inA = True
            self.flag['url'] = _attr('href',attrs)
        if self.inDiv and tag == 'span':
            self.inSpan = True

    def handle_endtag(self, tag):
        if tag == 'span':
            self.inSpan = False
    def handle_data(self, data):
        m = self.partten.match(data)
        if self.inSpan and m:
            self.flag['author'] = m.group()
            self.poem.append(self.flag)
            self.flag = {}
        if self.inA:
            self.inA = False
            self.flag['title'] = data




def _attr(name,list):
    for i in list:
        if i[0] == name:
            return i[1]
    return None
if __name__ == '__main__':

    # html = file('text.html')
    # print html.read()
    s = getAuthor()
    # s.feed(html.read())
    con = requests.get('http://so.gushiwen.org/gushi/tangshi.aspx')
    s.feed(con.content)
    print len(s.poem)
    for i in s.poem:
        print '%(url)s|%(title)s|%(author)s' % i
