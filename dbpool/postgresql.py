#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.
# momoko

from tornado import gen
from tornado.gen import Return, coroutine

import momoko
import sys


class mouriSAMA(object):
    def connect(self, ioloop, host, 
                dbname, user, passwd, port=5432):
        
        dsn = (("dbname=%s user=%s password=%s \
                host=%s port=%d" %(dbname, user, passwd, host, port)))

        self.db = momoko.Pool(dsn=dsn, 
                              size=5,
                              ioloop=ioloop)
        future = self.db.connect()
        ioloop.add_future(future, lambda x: ioloop.stop())
        ioloop.start()
        future.result()

    @coroutine
    def select(self, sql):
        cursor = yield self.db.execute(sql) 
        raise Return(cursor.fetchall())

    @coroutine
    def eropush(self, sql):
        yield self.db.execute(sql)


class Momoko(object):
    def connect(self, ioloop, host, 
                dbname, user, passwd, port=5432):
        
        dsn = (("dbname=%s user=%s password=%s \
                host=%s port=%d" %(dbname, user, passwd, host, port)))

        self.db = momoko.Pool(dsn=dsn, 
                              size=5,
                              ioloop=ioloop)
        future = self.db.connect()
        ioloop.add_future(future, lambda x: ioloop.stop())
        ioloop.start()
        try:
            future.result()
        except momoko.exceptions.PartiallyConnectedError, e:
            print "DB connection failed!! %s" %e
            sys.exit(0)

    @coroutine
    def insert(self, sql, **data):
        #sql_context = sql % data
        #yield self.db.execute(sql_context)
        yield self.db.execute(sql, data)

    @coroutine
    def select(self, sql, **data):
        #usql_context = sql % data
        #ucursor = yield self.db.execute(sql_context)
        cursor = yield self.db.execute(sql, data)
        raise Return(cursor.fetchall())
