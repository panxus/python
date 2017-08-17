import hashlib
import time

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







if __name__ == '__main__':
    # print(get_md5('baidu.com'))
    print(getUnixTime('2017-8/16','%Y/%m/%d'))
    pass