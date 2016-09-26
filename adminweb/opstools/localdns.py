#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from adminweb.handler.exception import WebErr
from functools import partial

import dns.zone
import re
import dns.query
import dns.update
import time

RRTYPE_LIST = {'1':"A", '2':"NS", '5':"CNAME", '6':"SOA", '12':"PTR", '15':"MX", '16':"TXT", '28':"AAAA", "33":"SRV", '39':"DNAME", '44':"DS"}


def _renovateRdata(regex, origin, rdtype, rdata):
    if rdtype == 5:
        if not re.match(regex, rdata):
            rdata = rdata + '.' + origin + '.'
    return rdata
    

def parseRecordFromFile(the_file, origin):
    regex = re.compile(r'.*\.$')
    zone = dns.zone.from_file(the_file, origin)
    record_list = [(str(name), str(ttl), RRTYPE_LIST[str(rdata.rdtype)], _renovateRdata(regex, origin, rdata.rdtype, str(rdata)), '1') 
                    for (name, ttl, rdata) in zone.iterate_rdatas() if rdata.rdtype is not 6]
    return record_list


class IxfrRecord:
    def __init__(self, origin, branch=None, master_server=None, port=53, keyring=None):
        self.dns_up = dns.update.Update(origin, keyring=keyring)
        assert master_server is not None
        self.master_server = master_server
        self.branch = str()
        self.port = port
        if branch is not None:
            self.chooseBranch(branch)
        self.query = partial(dns.query.tcp, where=self.master_server, port=self.port)

    def Delete(self):
        #print 'delete: '+self.sub_domain
        #print self.args
        self.dns_up.delete(self.sub_domain, *self.args)

    def Add(self):
        #print 'Add: '+self.sub_domain
        #print self.args
        self.dns_up.add(self.sub_domain, *self.args)

    def chooseBranch(self, branch):
        if 'delete' in branch:
            self.branch = 'Delete'
        if 'insert' in branch:
            self.branch = 'Add'

    def parseParams(self, **kw):
        '''
            kw = dict(
                src,
                dst
                )
            src,dst = dict(
                    sub_domain,
                    ttl,
                    record_type,
                    value,
                    mx,
                )
        '''
        self.sub_domain = kw.pop('sub_domain')
        args = list()
        if kw.has_key('ttl'): 
            args.append(int(kw.pop('ttl')))
        if kw.has_key('record_type'):
            args.append(str(kw.pop('record_type')))
        if kw.has_key('mx'):
            if kw['mx'] == '0': 
                del kw['mx']
            else:
                args.append(int(kw.pop('mx')))
        for a in kw.values():
            args.append(str(a))
        if 'Delete' in self.branch:
            del args[0]
        self.args = tuple(args)

    def post(self,  branch=None, **kw):
        if branch is not None:
            self.chooseBranch(branch)
        if self.branch is '': raise WebErr('Unknown branch value in it.')
        self.parseParams(**kw)
        func = 'self.' + self.branch
        eval(func)()
        result = self.query(self.dns_up)
        print result


def main():
    the_file = "/soft/Python2/scripts/opstools/tmp/bj2.daling.com"
    origin = 'bj2.daling.com'
    print parseRecordFromFile(the_file, origin)


if __name__ == '__main__':
    main()
