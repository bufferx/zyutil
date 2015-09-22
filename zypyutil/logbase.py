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

'''日志
'''

import os
import sys
import logging
import logging.handlers

def get_logger(app_name='main', f_path='/tmp/zy.log', log_level='DEBUG'):
    if not app_name or not f_path: 
        return None

    _logger = logging.getLogger(app_name)
    try:
        _logger.setLevel(getattr(logging, log_level.upper()))
    except AttributeError as e:
        _logger.setLevel(logging.DEBUG)

    bind_time_rotating(_logger, f_path)

    return _logger

def bind_time_rotating(logger, f_path):
    formatter = logging.Formatter('%(asctime)s - %(name)s - \
%(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(process)d - %(thread)d - %(message)s', '')
    f_handle = logging.handlers.TimedRotatingFileHandler(f_path, 'midnight', 1, 0)
    f_handle.setLevel(logging.DEBUG)
    f_handle.setFormatter(formatter)
    logger.addHandler(f_handle)

def main():
    ''' main function
    '''

if __name__ == '__main__':
    main()
