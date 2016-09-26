#!/usr/bin/env python
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding=utf-8 -*-
# Python by version 2.7.

from os.path import isdir
from yaml import load as yamlLoad
from re import match as re_match, search as re_search

import os
import sys


def _expYaml(d):

    fTmp = open(d)
    yTmp = yamlLoad(fTmp) # select for python dict
    fTmp.close()

    return yTmp


def parseParams(conf_Path):

    ''' trmap = ['record_api', 'config', 'domain_api', 'default'] '''

    found = filter(lambda x: isdir(x),
                    (conf_Path, '/etc/secdd/conf'))

    if not found:
        print "configuration directory is not exit!"
        sys.exit(0)

    recipe = found[0]
    trmap = dict()
    for root, dirs, files in os.walk(recipe):
        for filespath in files:
            if re_match('.*ml$', filespath):
                filename = re_search(r'(.*)\..*ml$', filespath).group(1)
                trmap[filename] = _expYaml(os.path.join(root, filespath))

    return trmap

