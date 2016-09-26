#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

def sqlZip(table_name, sql_data):
    return  map(lambda x: dict(zip(table_name, x)), sql_data)
