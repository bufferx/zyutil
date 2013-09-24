#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Zhang ZY<http://idupx.blogspot.com/> 
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''工具类测试
'''

import os
import sys
import time

import lib.tornado as tornado
from lib.tornado.options import define, options

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

options.app_name = 'PYUTIL_LOG_TEST'
options.log_level = 'DEBUG'
options.log_path = '/tmp'

from log import g_logger


def mb_test():
    from time_dedup_buffer import TimeDedupBuffer
    mb = TimeDedupBuffer(2)
    mb.add('K0', '0')
    mb.add('K0', '0')
    mb.add('K0', '0')
    mb.add('K1', '0')
    mb.add('K2', '0')
    mb.add('K1', '0')
    mb.add('K0', '0')
    mb.add('K2', '0')
    mb.add('K1', '0')
    mb.add('K3', '0')
    mb.add('K0', '0')
    mb.add('K0', '0')
    print mb.stats
    print [timeout for timeout in mb._timeouts]
    print mb._buckets
    print mb.get('K3')
    print mb.get('K0')

def http_test():
    from http import HttpUtil

    s = u'你好,世界{"k1":xxx, "k2":999}'
    s_encode = HttpUtil.urlencode(s)
    print 'OriUrl: %s' % s
    print 'Encode: %s' % s_encode
    print 'Decode: %s' % HttpUtil.urldecode(s_encode)
    print 'Done'
    pass

def common_test():
    from common import CommonUtil
    print CommonUtil.to_string(u'你好,世界')
    print CommonUtil.to_string(u'你好,世界', 'GBK')
    print CommonUtil.to_string(object)
    print CommonUtil.to_string(1024)
    print CommonUtil.to_unicode(u'你好,世界')
    print CommonUtil.to_unicode(CommonUtil.to_string(u'你好,世界', 'GBK'), 'GBK')
    s = 'jo4MDgwIinBhcmFt\t0ZWxpZCI6ICI0\ngsICJobATU4Iiwg\nInRhc2tb\x20DM2NDX19'
    print s
    print id(s)
    s_ = CommonUtil.re_str_replace(s, '\s', '')
    s = s.replace('\t', '')
    print s
    print id(s)
    print id(s_)
    print s_
    print CommonUtil.html_unescape('&lt;node&gt;&nbsp;value&nbsp;&lt;/node&gt;')
    print CommonUtil.re_str_replace('line0<br>newline', '\<br\>', '\n')
    print CommonUtil.re_str_replace(' encoding="utf-16"?>', 'encoding=\"utf-16\"', 'encoding="utf-8"')
    print CommonUtil.fibonacci_num(0) 
    print CommonUtil.fibonacci_num(1) 
    print CommonUtil.fibonacci_num(2) 
    print CommonUtil.fibonacci_num(3) 
    print CommonUtil.fibonacci_num(4) 
    print CommonUtil.fibonacci_num(5) 
    print CommonUtil.fibonacci_num(6) 
    print CommonUtil.fibonacci_num(7) 
    print CommonUtil.fibonacci_num(8) 
    print CommonUtil.fibonacci_num(9) 
    print CommonUtil.fibonacci_num(10) 
    # round robin
    dic = {
            'a': {
                'w': 5,
                'cc': 0,
                'sc': 0,
                },
            'b': {
                'w': 3,
                'cc': 0,
                'sc': 0,
                },
            'c': {
                'w': 2,
                'cc': 0,
                'sc': 0,
                },
            }
    for i in xrange(10):
        print CommonUtil.wdrr_schedule(dic, need_sc=True)
    print dic
    pass

def main():
    #http_test()
    #common_test()
    mb_test()

if __name__ == '__main__':
    main()
