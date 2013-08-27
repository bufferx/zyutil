#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Zhang ZY<http://idupx.blogspot.com/> 
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

'''Dedup Bucket
'''

from heapq import heappush
from heapq import heappop
import time

import assembly

class DedupBucket(object):

    __slots__ = ['_bucket', '_heap', '_capacity', '_dedup_time']

    @property
    def size(self):
        return len(self._bucket)

    def __init__(self, dedup_time=10, capacity=1024):
        assert dedup_time > 0
        assert capacity   > 0

        self._dedup_time  = dedup_time
        self._capacity    = capacity
        self._bucket      = {}
        self._heap        = []

    def get_data(self, k):
        if k not in self._bucket:
            return None

        now  = int(time.time())
        data = self._bucket[k] 

        if data['t'] >= now:
            return data['v']

        return None

    def add_data(self, k, v, now=None):
        def remove_data():
            while self._heap:
                _et, _k = heappop(self._heap)
                if _k != k:
                    del self._bucket[_k]
                    break
            pass

        if now is None:
            now  = int(time.time())

        expire_time = now + self._dedup_time
        
        if len(self._bucket) > self._capacity:
            remove_data()

        if k not in self._bucket:
            self._bucket[k] = {}

        data = self._bucket[k]
        data['t'] = expire_time
        data['v'] = v

        heappush(self._heap, k)
