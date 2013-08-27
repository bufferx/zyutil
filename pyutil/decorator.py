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

'''装饰器工具类
'''

import time
import re
import logging

try:
    from tornado.web import HTTPError
except Exception,e:
    from exceptions import Exception as HTTPError
    pass

import assembly

def time_it(_logger):
    '''统计函数执行时间
    '''
    def tmp(method):
        def wrapper(*args, **kwargs):
            assert isinstance(_logger, logging.Logger)
            _logger.debug('Func[%s] called by time_it', method.func_name)

            start_time = time.time()
            r = method(*args, **kwargs)
            delta_time = 1000.0 * (time.time() - start_time)

            _logger.debug('Func[%s] elapsed time: %.2fms' % (method.func_name, delta_time))

            return r
        return wrapper
    return tmp

def validate_ip(_logger, _pass=None):
    '''验证IP白名单
    '''
    def tmp(method):
        def wrapper(self, *args, **kwargs):
            assert isinstance(_logger, logging.Logger)
            _logger.debug(
                    'Func[%s] called by validate_ip', 
                    method.func_name
                    )

            remote_ip = self.request.remote_ip
            ip_list = \
                re.findall('(192.168.0.\d{1,3}|127.0.0.\d{1,3})', remote_ip, re.DOTALL)
            if not ip_list:
                if _pass is None or _pass != 'NDY':
                    raise HTTPError(403)
            _logger.debug('valid ip: %s', ip_list)

            r = method(self, *args, **kwargs)
            return r
        return wrapper
    return tmp
