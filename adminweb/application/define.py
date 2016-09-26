#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

#import tornado.options
from tornado.options import define


define("PORT", type=int)
define("SERVER", type=str)
define("LOGINUSER", type=str)
define("LOGINPASS", type=str)
define("DEBUG", type=bool, default=False)
