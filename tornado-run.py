#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from yaml import load as yamlLoad
from os.path import isdir
from re import match as re_match, search as re_search, split as re_split

from smalltools.parseConfig import parseParams
from dbpool.postgresql import Momoko
from adminweb.application.Application import WebApplication
from ownutils.todoredis import NonAsyncRedis

from tornado.options import options

import adminweb.application.define

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def main():
    file_path = os.path.split(os.path.realpath(__file__))[0] + '/'
    config_file = file_path + 'web-conf.d/default.conf'
    form_path = file_path + 'forms'
    extend_config_path = file_path + 'conf.d/'
    extend_config = parseParams(extend_config_path)
    redis_config = extend_config['redis']
    db_conf = extend_config['db']
    tornado.options.parse_config_file(config_file)
    io_loop = tornado.ioloop.IOLoop.instance()
    application = WebApplication()
    application.redis = NonAsyncRedis(redis_config['server'], redis_config['port'],redis_config['db'])
    #application.setting['debug'] = options.DEBUG
    application.forms = parseParams(form_path)
    application.db = Momoko()
    application.db.connect(io_loop, db_conf['DBSERVER'], db_conf['DBNAME'],
                           db_conf['DBUSER'], db_conf['DBPASS'], db_conf['PORT'])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.PORT)
    io_loop.start()


if  __name__ == '__main__':

    main()
