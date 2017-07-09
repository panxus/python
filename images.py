#coding=utf-8
import requests
import urllib
import os
import threading

gImageList = []
gCond = threading.Condition()

class producer(threading.Thread):
    def run(self):
        global gImageList
        global gCond
        print 'producer threading started at %s' % threading.current_thread()
        imgs = HandleBaiduImage()
        gCond.acquire()
        for i in imgs:
            if 'imageUrl' in i :
                gImageList.append(i['imageUrl'])
        print 'producer threading ended at %s,left %s' % (threading.current_thread(),len(gImageList))
        gCond.notify_all()
        gCond.release()

class Customer(threading.Thread):
    def run(self):
        print 'Customer threading started at %s' % threading.current_thread()
        while True:
            global gImageList
            global gCond

            gCond.acquire()
            print 'trying download  at %s,left %s' % (threading.current_thread(),len(gImageList))
            while len(gImageList) ==0:
                gCond.wait()
                print 'waiting  at %s,left %s' % (threading.current_thread(),len(gImageList))
            url = gImageList.pop()
            gCond.release()
            downImages(url)

def _fname(url,path):
    return os.path.join(path,os.path.split(url)[1])

def downImages(url,path='images'):
    print 'threading started at %s' % threading.current_thread()
    print 'now downing %s' % url
    if not os.path.isdir(path):
        os.mkdir(path)
    urllib.urlretrieve(url,_fname(url,path))
    print 'threading ended at %s' % threading.current_thread()



def HandleBaiduImage():
    url = 'http://image.baidu.com/data/imgs'
    param = {
        'pn':'0',
        'rn':'24',
        'col':'壁纸',
        'tag':'全部',
        'tag3':'',
        'width':'1366',
        'height':'768',
        'ic':'0',
        'ie':'utf8',
        'oe':'utf-8',
        'image_id':'',
        'fr':'channel',
        'p':'channel',
        'from':'1',
        'app':'img.browse.channel.wallpaper',
        't':'0.24067399592890237',
    }
    res = requests.get(url,params=param)
    result = res.json()
    imgs = result['imgs']
    print '%s ,images total %s' % (threading.current_thread(),len(imgs))
    return imgs

if __name__ == '__main__':
    producer().start()

    for i in range(2):
        Customer().start()
    pass