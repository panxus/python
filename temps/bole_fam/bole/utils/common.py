import time
import hashlib

def get_md5(url):
    if isinstance(url,str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def getUnixTime(timeStr,type):
    try:
        s = time.mktime(time.strptime(timeStr,type))
    except Exception as e:
        return ''
    else:
        return s

if __name__ == '__main__':
    print(get_md5('baidu.com'))

    print(getUnixTime('2017-08-16','%Y-%m-%d'))
    pass

