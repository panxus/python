#coding=utf-8
import re

# str = '13476852459'
# str = '134-7685-2459'
# str = '+8613476852459'
str = '+86134-7685-2459'


s = re.compile(r'''
    (\+86)? # 前缀可有可无
    \d{3}   # 手机号前三位
    -?      # 可有可无
    \d{4}   # 手机号
    -?      # 可有可无
    \d{4}   # 手机号
''',re.VERBOSE)


print re.search(s,str).group()
