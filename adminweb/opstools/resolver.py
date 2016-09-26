#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from dns.resolver import Resolver, NoAnswer

import time


#RRTYPE_LIST = dict(1="A", 2="NS", 5="CNAME", 6="SOA", 12="PTR", 15="MX", 16="TXT", 28="AAAA", 33="SRV", 39="DNAME", 44="DS")

class CheckDns:
    def __init__(self, nameserver):
        self.resolver = Resolver()
        self.resolver.nameservers = [nameserver]
        self.nameserver = nameserver

    def Status(self, record, rdtype):
        re_dict = dict(records=None, time=None, nameserver=self.nameserver)
        #res = self.resolver.query('www.daling.com')
        #print res
        try:
            time_in = time.time()
            res = self.resolver.query(record, rdtype).response.answer
            time_out = time.time()
            do_time = time_out - time_in
            res_l =  [l for r in res for l in r.__str__().split('\n')]
            re_dict['records'] = res_l
            re_dict['time'] = do_time
            re_dict['status'] = True
        except NoAnswer, e:
            re_dict['records'] = e
            re_dict['status'] = False
        return re_dict


# detail 
#class CheckDns:
#    def __init__(self, nameserver):
#        self.resolver = Resolver()
#        self.resolver.nameservers = [nameserver]
#
#    def Status(self, record):
#        try:
#            res = self.resolver.query(record).response.answer
#        except dns.resolver.NoAnswer, e:
#            return [False, e]
#        g = lambda x: eval("__" + RRTYPE_LIST.get(x.rdtype))(x, x.ttl) if x.rdtype in RRTYPE_LIST else dict(rdtype=x.rdtype, status='Unknown type.')
#        res_dict = map(lambda x: g(x), res)
#        return [True, res_dict]
#
#    def __A(self, func, ttl):
#        return __resultDict(func.rdtype, func.address, ttl)
#
#    def __CNAME(self, func, ttl):
#        return __resultDict(func.rdtype, func.target, ttl)
#
#    def __NS(self, func, ttl):
#        return __resultDict(func.rdtype, func.target, ttl)
#
#    def __MX(self, func, ttl):
#        return __resultDict(func.rdtype, func.exchange, ttl, preference=func.preference)
#
#    def __TXT(self, func, ttl):
#        return __resultDict(func.rdtype, func.strings, ttl)
#
#    def __resultDict(self, rdtype, address, ttl, **kw):
#        the_dict = dict(rdtype=rdtype,
#                        address=address,
#                        ttl=ttl)
#        the_dict.update(**kw)
#        the_dict['status'] = 'Ok.'
#        return the_dict

    



