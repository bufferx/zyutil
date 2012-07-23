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

'''通用工具类
'''

import os
import sys
import time
import re

import assembly

_STR_TYPES = (str, type(None))
_UNICODE_TYPES = (unicode, type(None))

class CommonUtil(object):
    @staticmethod
    def to_string(value, encoding='utf-8'):
        '''Reference: tornado.escape.utf8()
        Converts a string argument to a byte string.

        If the argument is already a byte string or None, it is returned
        unchanged.

        And if it is a unicode string and is encoded as specified
        encoding which default 'utf-8'.

        Otherwise Cast to a string enforcedly.
        '''
        if isinstance(value, _STR_TYPES):
            return value

        if isinstance(value, _UNICODE_TYPES):
            result = value.encode(encoding, 'ignore')
        else:
            result = str(value)
        return result

    @staticmethod
    def to_unicode(value, encoding='utf8'):
        '''Reference: tornado.escape.to_unicode()
        Converts a string argument to a unicode string.

        If the argument is already a unicode string or None, it is returned
        unchanged.  

        Otherwise it must be a byte string and is decoded as utf8.
        '''
        if isinstance(value, _UNICODE_TYPES):
            return value

        assert isinstance(value, str)
        result = value.decode(encoding, 'ignore')
        return result

    @staticmethod
    def re_str_replace(s, pattern, dist):
        '''pattern/dist must be StringType
        '''
        s = CommonUtil.to_string(s)
        strinfo = re.compile(pattern)
        return strinfo.sub(dist, s)

    @staticmethod
    def time_format(_time=time.localtime(), pattern = '%Y-%m-%d %H:%M:%S'):
        return time.strftime(pattern, _time)

    @staticmethod
    def make_dir(file_name):
        file_dir = os.path.dirname(file_name)
        if not os.path.exists(file_dir):
            return os.makedirs(file_dir)
        return False

    @staticmethod
    def get_cur_info_4_log():
        '''
        Return the frame object for the caller's stack frame.
        '''
        try:
            raise Exception
        except:
            f = sys.exc_info()[2].tb_frame.f_back
        return (f.f_code.co_name, f.f_lineno)

    @staticmethod
    def fibonacci_num(n):
        if n == 0 or n == 1:
            return n 
        else:
            a, b = 0, 1
            for i in xrange(n - 1): 
                c = a + b 
                a, b = b, c
            return c

def main():
    pass

if __name__ == '__main__':
    main()
