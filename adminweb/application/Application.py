#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from adminweb.handler.token import AccessTokenHandler

from tornado.web import Application
from tornado.options import options


class WebApplication(Application):
    def __init__(self):
        handlers = [(r"/api/token", AccessTokenHandler)]
        settings = dict(
                        cookie_secret = "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                        #login_url = "/login",
                        debug=options.DEBUG
                       )
        print "DEBUG Options is %s." %options.DEBUG
        Application.__init__(self, handlers, **settings)

