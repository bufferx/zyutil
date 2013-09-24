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

'''HTTP相关工具类
'''

import os
import sys
import re
import urllib

try:
    from tornado.web import HTTPError
except Exception,e:
    from exceptions import Exception as HTTPError
    pass

from common import CommonUtil

class HttpUtil(object):
    @staticmethod
    def urlencode(value, encoding='utf-8'):
        value = CommonUtil.to_string(value)
        return urllib.quote(value)

    @staticmethod
    def urldecode(value):
        value = CommonUtil.to_string(value)
        return urllib.unquote(value)

    @staticmethod
    def get_header_string(request):
        '''header增加反向代理透传的真实IP
        '''
        request.headers['Real-Clientip'] = request.remote_ip
        return request.headers

    @staticmethod
    def validate_ip(request, _pass=None):
        '''验证IP白名单
        '''
        remote_ip = request.remote_ip
        ip_list = \
            re.findall('(192.168.0.\d{1,3}|127.0.0.\d{1,3})', remote_ip, re.DOTALL)
        if not ip_list:
            if _pass is None or _pass != 'NDY':
                raise HTTPError(403)
        return

def main():
    pass

if __name__ == '__main__':
    main()
