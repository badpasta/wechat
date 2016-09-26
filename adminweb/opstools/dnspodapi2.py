#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Python by version 2.7.
# pip install pyYaml requests==2.5.3 json argparse
#

from smalltools.opsJson import jsonLoads, convJson, convSimpleJson
from adminweb.handler.exception import WebErr

from tornado.gen import coroutine, Task, Return
from tornado.httpclient import AsyncHTTPClient

import urllib
import requests # select to http://docs.python-requests.org/en/latest/user/quickstart/
import os
import sys
import time

# Operation Dnspod.
class BaseRequestUrl:

    def __init__(self, line, **kwargs):

        self.uData = dict(record_line=line)
        self.uHeaders = {"content-type": "application/x-www-form-urlencoded", 
                         "accept": "text/json", 
                         "user-agent": "dldnspod-python/0.01 wangjingyu@daling.com; dnspod.cn api v2.8)"}
        self.uData.update(**kwargs)

    @coroutine
    def urlPost(self, u, **kw):

        result = [bool(),str()]
        uApi = u
        self.uData.update(**kw)
        #if 'Domain' in u: del self.uData['record_line']
        body = urllib.urlencode(self.uData)
        #print u
        #print self.uData
        httpclient = AsyncHTTPClient()
        uPost = yield httpclient.fetch(uApi, method='POST', body=body, headers=self.uHeaders)
        #print uPost.body
        try:
            jPost = jsonLoads(uPost.body)
            #print jPost
            if jPost.get("status", {}).get("code") == "1":
                result[0] = True
                result[1] = jPost
            else:
                result[0] = False
                result[1] = jPost
                #raise Exception(jPost['status'])
        except:
            result[0] = False
            result[1] = uPost.body
        raise Return(result)


@coroutine
def domainId(func, domain, api, **kw):
    result = [bool(),str()]
    the_list = yield Task(func.urlPost, api)
    if the_list[0] is False: raise Return(the_list)
    domain_list = filter(lambda domain_dict: domain in domain_dict.values(), the_list[1]['domains'])
    #time.sleep(1)
    domain_id = domain_list[0].get('id')
    result[0]= True
    result[1] = domain_id
    raise Return(result)


@coroutine
def pushDNS(request_func, branch, domain_id, **kw): 
    '''
        login_token
        format
        domain_id
        sub_domain
        record_type
        record_line
        value
    '''
    result = [bool(),str()]
    message = None
    api = kw['api']['record'][branch]
    udata = dict(kw['record'])
    udata.update(domain_id=domain_id)
    if udata.get('description'): del udata['description']
    if udata.get('zid'): del udata['zid']
    if udata.get('rgid'): del udata['rgid']
    print udata['status'] 
    if udata['status'] == 'True':
        udata['status'] = 'enable'
    else:
        udata['status'] = 'disable'
    if udata['record_type'] is not 'MX':
        del udata['mx']
    elif udata['mx'] > 20 and udata['mx'] < 1:
        message = 'MX value must gt 1 and lt 20.'
    if udata['weight'] > 100 and udata['weight'] < 0:
        message = 'weight value must gt 0 and lt 100.'
    if message is not None: raise Return(list(False, message))
    the_list = yield Task(request_func.urlPost, api, **udata)
    raise Return(the_list)


class PushDNS:
    def __init__(self, request_func, domain_id, api):
        '''
            kw.keys = (
            login_token,
            format,
            domain_id,
            sub_domain,
            record_type,
            record_line,
            value)
        '''
        self.func = request_func
        self.api = api
        self.udata = dict(domain_id=domain_id)

    def parseParams(self, kw):
        if kw.get('description'): del kw['description']
        if kw.get('zid'): del kw['zid']
        if kw.get('rgid'): del kw['rgid']
        if kw.has_key('rid'):
            kw['record_id'] = kw.pop('rid')
        if kw['status']:
            kw['status'] = 'enable'
        else:
            kw['status'] = 'disable'
        message = None
        if kw['record_type'] is not 'MX':
            del kw['mx']
        elif kw['mx'] > 20 and kw['mx'] < 1:
            message = 'MX value must gt 1 and lt 20.'
        if kw['weight'] > 100 and kw['weight'] < 0:
            message = 'weight value must gt 0 and lt 100.'
        if message is not None: raise WebErr(messge)
        return kw

    @coroutine
    def post(self, **kw):
        self.udata.update(self.parseParams(kw))
        the_list = yield Task(self.func.urlPost, self.api, **self.udata)
        raise Return(the_list)
        
    
class PickCookie:
    def __init__(self, **kw):
        '''
        # Test Data
        sub_domain = 'A'
        record_line = 'A'
        value = 'A'
        record_type = 'A'
        ttl = '60'
        weight = '0'
        mx = '0'
        status = 'True'
        rgid = '1'
        zid = '123'
        description = ''
        '''
        # Use Data
        sub_domain = kw.get('name', str())
        record_type = kw.get('type', str())
        value = kw.get('value', str()) 
        ttl = kw['ttl'] or '60'
        weight = kw['weight'] if kw.get('weight') else '0'
        #mx = '0' if 'mx' not in record_type else kw.get('mx', '0') 
        mx = '0' if 'MX' not in record_type else kw.get('mx', '0') 
        record_line = kw.get('line', str(u'默认'))
        status = True if '1' in kw.get('enabled', '0') else False
        rgid = kw.get('rgid', '1')
        zid = kw.get('zid')
        description = kw.get('description', '')
        #
        self.record = dict(
            sub_domain = sub_domain, 
            record_type = record_type, 
            value = value, 
            ttl = ttl,
            weight = weight,
            mx = mx,
            record_line = record_line,
            status = status,
            rgid = rgid,
            zid = zid,
            description = description
            )
        if kw.has_key('id'): 
            self.record.update(rid = kw['id'])

    def _PickCookie(self):
        return self.record

    __call__ = _PickCookie

