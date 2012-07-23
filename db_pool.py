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

'''数据库连接池工厂类
依赖于options
'''

import threading
import MySQLdb
import DBUtils.PersistentDB
import DBUtils.PooledDB

from lib.tornado.options import options

class DBPoolFactory(object):

    TYPE_POLLEDDB = 0
    TYPE_PERSISTENTDB = 1

    @staticmethod
    def create(db_type):
        _db_pool = None
        if db_type == DBPoolFactory.TYPE_POLLEDDB:
            _db_pool = DBUtils.PooledDB.PooledDB( \
                    MySQLdb, \
                    maxusage=options.db_maxusage, \
                    **conn_kwargs)
        elif db_type == DBPoolFactory.TYPE_PERSISTENTDB:
            _db_pool = DBUtils.PersistentDB.PersistentDB( \
                    MySQLdb, \
                    maxusage=options.db_maxusage, \
                    **conn_kwargs)
            pass
        return _db_pool
