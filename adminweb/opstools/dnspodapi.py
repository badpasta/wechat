#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.
# pip install pyYaml requests==2.5.3 json argparse
#

from json import loads as json_loads, dumps as json_dumps

import requests # select to http://docs.python-requests.org/en/latest/user/quickstart/
import os
import sys


# Operation Dnspod.
class BaseRequestUrl:

    def __init__(self, **kwargs):

        self.uData = dict()
        self.uheaders = {"content-type": "application/x-www-form-urlencoded", 
                         "accept": "text/json", 
                         "user-agent": "dldnspod-python/0.01 wangjingyu@daling.com; dnspod.cn api v2.8)"}
        self.uData.update(**kwargs)


    def urlPost(self, u, **kw):

        uApi = u
        #print self.uData
        uPost = requests.post(url=uApi,
                              data=self.uData, 
                              headers=self.uHeaders).content #request.post(url=,headers=,data=,..)

        try:
            jPost = json_loads(uPost)
#            if jPost.get("status", {}).get("code") == "1":
            return jPost
#            else:
#                raise Exception(jPost)
        except:
            return uPost  
            #sys.exit(0)


class DomainList(BaseRequestUrl):

    pass


def DomainId(api, domain, **kw):

    ''' dInfo = [{},{}]
        login_token = userid + , + token
        output_format = json or xml 
        kw = { 'format' =,
               'login_token' = }'''

    dInfo = DomainList(**kw).urlPost(api).get("domains", {})
    #dId = [d.get('id') for d in dInfo if domain in d.values()] ## Esay by list? And dnspod domain api was not supported like "*".
    #dId = ''.join([str(d.get('id')) for d in dInfo if domain in d.values()]) ## It's so inconvenient.
    dId = ''
    for dictionary in dInfo:
        if domain in dictionary.values():
            dId = dictionary.get("id")
            break

    #dId = [d.get('id') for d in dInfo if domain in d.values()][0]

    return dId
    

class RecordList(BaseRequestUrl):

    def __init__(self, domain_id, **kw):

        '''kw = { format = output_format,
                  login_token = login_token,
                  domain_id = domain_id} '''
        
        kwargs = {"domain_id":domain_id}
        kwargs.update(**kw)
        
        BaseRequestUrl.__init__(self,  **kwargs)


class RecordCreate(RecordList):

    pass


class RecordMuticreate(RecordList):

    pass


class RecordRemove(BaseRequestUrl):

    def __init__(self, domain_id, record_id, **kwargs):

        ''' {format:
             token:
            }'''

        kw = {'domain_id': domain_id,
              'record_id': record_id}
        kw.update(**kwargs)

        BaseRequestUrl.__init__(self, **kw) 
        

class RecordModify(RecordRemove):

    pass


class RecordInfo(RecordRemove):

    pass


class RecordDisable(RecordRemove):

    pass
# -----
           



