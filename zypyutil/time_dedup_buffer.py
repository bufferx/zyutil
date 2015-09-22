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

'''Time Dedup Buffer
'''

from collections import deque
try:
    from monotime import monotonic as time
except ImportError:
    from time import time


class TimeDedupBuffer(object):

    __slots__ = ['_buckets', '_timeouts', '_capacity', '_timeout']

    @property
    def stats(self):
        return {'size': len(self._buckets),
                'capacity': self._capacity,
                'timeout_size': len(self._timeouts)
               }
        return len(self._buckets)

    def __init__(self, capacity=1024, timeout=10):
        assert capacity   > 0

        self._capacity    = capacity
        self._buckets     = {}
        self._timeouts    = deque(maxlen=capacity + 1)
        self._timeout     = timeout

    def _set(self, k, v):
        def remove_data():
            k = self._timeouts.popleft()
            del self._buckets[k]

        if len(self._buckets) >= self._capacity:
            remove_data()

        data = {}
        data['t'] = time() + self._timeout
        data['v'] = v

        self._timeouts.append(k)

        self._buckets[k] = data

    def get(self, k):
        '''Retrieval command
        '''
        if k not in self._buckets:
            return None

        now  = time()
        data = self._buckets[k]

        if data['t'] > now:
            return data['v']

        self.delete(k)
        return None

    def add(self, k, v):
        '''Storage command
        '''
        data = self.get(k)

        if data is not None:
            return 'NOT_STORED'

        self.set(k, v)

        return 'STORED'

    def set(self, k, v):
        '''Storage command
        '''
        self.delete(k)

        self._set(k, v)

        return 'STORED'

    def delete(self, k):
        try:
            self._timeouts.remove(k)
            del self._buckets[k]
            return 'DELETED'
        except (KeyError, ValueError) as e:
            return 'NOT_FOUND'
