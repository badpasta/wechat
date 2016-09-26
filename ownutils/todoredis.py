#!/usr/bin/env python
# -*- coding: utf-8 -*-
# # Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# Python by version 2.7.

from redis import ConnectionPool,Redis

from contextlib import contextmanager


class NonAsyncRedis(object):
    def __init__(self, server='127.0.0.1', port=6379,db=0): 
        pool = ConnectionPool(host=server, port=port,db=db)
        self.redis = Redis(connection_pool=pool)
        self.pipe = self.redis.pipeline()

    def push(self, param, key, args):
        #self.redis.delete(key)
        if not self.redis.llen(key):
            p = eval('self.pipe.'+param)
            p(key, *args)
            self.pipe.execute()
        #print "key:%s" %key
        return
        #print "key:%s" %key
        #print  "redis push done."

    def parseData(self, key, *args): pass
        
