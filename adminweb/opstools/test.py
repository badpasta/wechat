#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

import resolver
import sys

nameserver = '10.0.26.116'
c = resolver.CheckDns(nameserver)
d = c.Status(sys.argv[1], sys.argv[2])

print d
