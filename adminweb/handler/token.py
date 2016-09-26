#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# Python by version 2.7.


from adminweb.handler.base import BaseHandler
from adminweb.handler.exception import WebErr
from smalltools.opsJson import jsonLoads, convJson, convSimpleJson
from smalltools.status import Message
from smalltools.Other import sqlZip

from tornado.gen import coroutine, Task, Return
from tornado.httpclient import AsyncHTTPClient
from functools import partial

import time
import sys
import hashlib

class AccessTokenHandler(BaseHandler):
    @coroutine
    def get(self):
        origin_data = dict()
        try:
            origin_data['signature'] = self.get_argument('signature')
            origin_data['timestamp'] = self.get_argument('timestamp')
            origin_data['nonce'] = self.get_argument('nonce')
            origin_data['echostr'] = self.get_argument('echostr')
        except:
            self.write('param failed!')
            return
        echostr = origin_data['echostr']
        kw = dict()
        sql = 'select token, aeskey, issecret from wechat_info;'
        wechat_info = yield Task(self.db.select, sql, **dict())
        #print wechat_info[0][0].strip()
        #print 'timestamp:'+origin_data['timestamp']
        #print origin_data['nonce']
        kw['token'] = wechat_info[0][0].strip()
        kw['timestamp'] = origin_data['timestamp']
        kw['nonce'] = origin_data['nonce']
        secret = ''.join(sorted(kw.values()))
        sha1_secret = hashlib.sha1(secret).hexdigest()
        #print sha1_secret
        #print origin_data['signature']
        if sha1_secret == origin_data['signature']:
            self.write(echostr)
        else:
            self.write('error')
            return

