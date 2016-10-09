#!/usr/bin/env python
# -*- coding: utf-8 -*-
# # Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# Python by version 2.7.


from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado.gen import coroutine, Task, Return
from adminweb.handler.exception import WebErr


import types
import urllib
import requests

class AsyncHttpClient(object):
    def __init__(self, user_agent=''):
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36" if not len(user_agent) else user_agent
        self.headers = dict()
        AsyncHTTPClient.__init__(self)

    def setHeaders(self, **kw):
        '''dict("User-Agent":user_agent,"Host":host)'''
        self.headers.update(**kw)

    def header_dict(self, host='', user_agent=''):
        agent = user_agent if len(user_agent) else self.user_agent
        return  {
                    "User-Agent": agent,
                    "Host":host
                 }

    @property
    def http_client(self):
        return AsyncHTTPClient()

    def request(self, method, *args):
        url = str()
        if len(args) == 2:
            url = args[0] + args[1]
        elif len(args) == 1:
            url = args[0]
        else:
            raise WebErr('AsynchttpClient Request params err!')
        return HTTPRequest(url=url,headers=self.headers, method=method) 

    @coroutine
    def push(self, request,  method='GET', *args):
        http_request = None
        if isinstance(request, types.MethodType):
            http_request = self.request(method, *args)
        else:
            http_request = request
        result = yield self.http_client.fetch(http_request)
        raise Return(result)

    def getUrl(self, url_list, method='GET', **headers):
        http_headers = self.setHeaders(**headers)
        for url in url_list:
            request = self.request(method, url)
            yield request



class RequestUrl:
    def __init__(self, **kwargs):
        self.uData = dict()
        self.uHeaders = {"content-type": "application/x-www-form-urlencoded", 
                         "accept": "text/json", 
                         "user-agent": "other-python/0.01 soversion@hotmail.com; weixin api v1.0"}
        self.uData.update(**kwargs)

    def urlGet(self, u, **kw):
        uApi = u
        self.uData.update(**kw)
        result_data = requests.get(u,params=self.uData)
        if 200 != result_data.status_code:
            print result_data.json()
            raise ValueError
        print 'request return'
        return result_data.json()


