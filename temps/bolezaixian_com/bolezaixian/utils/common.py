import hashlib
import time
import re
def get_md5(url):
    if isinstance(url,str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def getUnixTime(str,type):
    # type = '%Y-%m-%d %H:%M:%S'
    try:
        s = int(time.mktime(time.strptime(str,type)))
    except Exception as e:
        return 0
    else:
        return s


def date_handle(val):
    vals = val.replace('·','').strip()
    try:
        s = time.mktime(time.strptime(vals,'%Y/%m/%d'))
    except Exception as e:
        return 0
    else:
        return int(s)


def url_handle(val):
    return val


def ob_handle(url):
    if isinstance(url,str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def nums_handle(val):
    s = re.search('(\d+)',val)
    if s:
        return s.group(1)
    else:
        return 0

def get_now_unix(val):
    return int(time.time())

if __name__ == '__main__':
    # print(get_md5('baidu.com'))
    # print(getUnixTime('2017-8/16','%Y/%m/%d'))
    print(int(time.time()))
    pass