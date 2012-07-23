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

'''全局日志实例
依赖于options
'''

import os
import sys

from logbase import get_logger
from lib.tornado.options import options

g_logger = get_logger(options.app_name, '%s/%s.Main.log' % (options.log_path, \
    options.app_name), options.log_level.lower())

def main():
    g_logger.debug('Debug.....')
    g_logger.info('Info.......')
    g_logger.warning('Warning.....')
    g_logger.error('Error......')
    g_logger.fatal('Critical.....')
    g_logger.debug('Debug......')

if __name__ == '__main__':
    main()
