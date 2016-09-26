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

import dns.reversename
import time
import sys
import hashlib

class AccessTokenHandler(BaseHandler):
    @coroutine
    def get(self):
        origin_data = dict()
        origin_data['signature'] = self.get_argument('signature')
        origin_data['timestamp'] = self.get_argument('timestamp')
        origin_data['nonce'] = self.get_argument('nonce')
        origin_data['echostr'] = self.get_argument('echostr')
        echostr = origin_data['echostr']
        secret = ''.join(origin_data.values())
        sha1_secret = hashlib.sha1(secret).hexdigest()
        self.write(sha1_secret)
            

