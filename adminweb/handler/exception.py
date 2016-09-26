#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.


class WebErr(Exception):
    def __init__(self, message):
        if isinstance(message, str):
            self.message = message
        else:
            raise WebErr('Err: value type not str!')
        #Exception.__init__(self,self.message)  

    def __str__(self):                                                                    
        return repr(self.message)
