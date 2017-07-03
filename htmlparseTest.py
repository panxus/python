import requests
from HTMLParser import HTMLParser
class DMusic(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._MUSIC = []
        self._inDiv = False
        self._inA = False
        self._inP = False
        self._inSpan = False

    def handle_starttag(self, tag, attrs):
        def _attr(name,list):
            for i in list:
                if i[0] == name:
                    return i[1]
            return None
        if tag =='div' and _attr('class',attrs) == 'album-item':
            self._inDiv = True
        if self._inDiv and tag == 'img':
            mus = {}
            mus['img-url'] = _attr('src',attrs)
            self._MUSIC.append(mus)
            downMusicImg(_attr('src',attrs))
        if self._inDiv and tag == 'a' and _attr('class',attrs) == 'album-title':
            self._inA = True
        if self._inDiv and tag == 'p':
            self._inP = True
        if self._inDiv and tag == 'span' and _attr('class',attrs) == 'score':
            self._inSpan = True
            self._inDiv = False

    def handle_data(self, data):
        index = len(self._MUSIC) - 1
        if self._inA:
            self._inA = False
            self._MUSIC[index]['music'] = data
        if self._inP:
            self._inP = False
            self._MUSIC[index]['singer'] = data
        if self._inSpan:
            self._inSpan = False
            self._MUSIC[index]['score'] = data

def downMusicImg(url):
    fname = url.split('/')[-1]
    content = requests.get(url)
    with open(fname,'wb') as f:
        f.write(content.content)


if __name__ == '__main__':
    s = DMusic()
    # head = {'User-Agent':'Mozilla/5.0 (WindowsNT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Host':'music.douban.com','Upgrade-Insecure-Requests':'1'}
    # con = requests.get('https://music.douban.com/',headers=head)
    # print con.content
    # s.feed(con.content)
    # con = open('./douTest.html')
    # s.feed(con.read())
    # con.close()
    # print s._MUSIC
    # f = file('result.txt','w+')
    # for i in s._MUSIC:
    #     con = 'music:{0},singer:{1},score:{2},img:{3}'.format(i['music'],i['singer'],i['score'],i['img-url'].split('/')[-1])
    #     f.write(con)
    #     f.write('\n')
    # f.close()
