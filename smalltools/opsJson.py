#!/usr/bin/env python
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding=utf-8 -*-
# Python by version 2.7.

from json import  dumps as json_dumps, loads as json_loads


def convJson(url):

    return json_dumps(url,sort_keys=True, indent=4)

def convSimpleJson(url):

    return json_dumps(url)


def jsonLoads(url):

    return json_loads(url)

