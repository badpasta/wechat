#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from smalltools.Other import sqlZip

from tornado.gen import coroutine, Task, Return
from tornado.httpclient import AsyncHTTPClient

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    @property
    def db(self):
        return self.application.db

    @property
    def redisClient(self):
        return self.application.redis

    @property
    def forms(self):
        return self.application.forms

    @property
    def the_box(self):
        self.box = dict()
        self.box['title'] = 'badpasta.com'
        return self.box

    @property
    def http_Client(self):
        return AsyncHTTPClient()

