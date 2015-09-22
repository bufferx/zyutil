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

import logging

from hashlib import md5, sha1


LOG = logging.getLogger()


class ConsistentHash(object):
    '''Implement Consistent Hashing
    '''

    DEFAULT_PADDING     = '#'

    NODE_FMT = '{service}#{idx}'.format

    @property
    def hashring(self):
        if not hasattr(self, '_HASH_RING'):
            self.__init_hashring()

        return self._HASH_RING

    def __init__(self, hash_range=65536, hash_func='md5'):
        """
        """
        self._HASH_RANGE = hash_range
        self.__init_hashring()

        try:
            self._hash_method = getattr(self, '_hash_%s' % hash_func)
        except AttributeError as e:
            LOG.warn(e, exc_info=True)
            self._hash_method = hash_func

    def _hash_md5(self, k):
        return int(md5(k).hexdigest(), 16)

    def _hash_sha1(self, k):
        return int(sha1(k).hexdigest(), 16)

    def __init_hashring(self):
        self._HASH_RING = [self.DEFAULT_PADDING] * self._HASH_RANGE

    def __get_hashring_index(self, key):
        return self._hash_method(key) % self._HASH_RANGE

    def update(self, nodes):
        """Update Hash Ring With Nodes

        nodes is a list of ($SERVER, $WEIGHT), e.g.:
        nodes = [('10.0.33.2:11211', 20), ('10.0.33.3:11211', 30)]
        """
        self.__init_hashring()

        for service, weight in nodes:
            for i in xrange(weight):
                _node = self.NODE_FMT(service=service, idx=i)
                index = self.__get_hashring_index(_node)
                self._HASH_RING[index] = service

        last_service = self.DEFAULT_PADDING
        for idx in reversed(xrange(self._HASH_RANGE)):
            if self._HASH_RING[idx] != self.DEFAULT_PADDING:
                last_service = self._HASH_RING[idx]
                continue
            if last_service != self.DEFAULT_PADDING:
                self._HASH_RING[idx] = last_service

        for idx in reversed(xrange(self._HASH_RANGE)):
            if self._HASH_RING[idx] != self.DEFAULT_PADDING:
                break
            self._HASH_RING[idx] = last_service

    def dispatch(self, key):
        """Dispatch Service By Key

        ASSERT isinstance (key, str)
        """
        index = self.__get_hashring_index(key)
        return self._HASH_RING[index]
