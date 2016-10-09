#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# Python by version 2.7.

from psycopg2 import connect
from smalltools.parseConfig import parseParams
from adminweb.opstools.http import AsyncHttpClient, RequestUrl
from smalltools.opsJson import jsonLoads, convJson, convSimpleJson

from contextlib import contextmanager

import os
import datetime
import time


class SyncPG(object):
    def __init__(self, **config):
        self.config_dict =  dict(
            database = config['DBNAME'],
            user = config['DBUSER'],
            password = config['DBPASS'],
            host = config['DBSERVER'],
            port = config['PORT']
            )

    @contextmanager
    def execute_base(self):
        #self.conn = connect(**self.config_dict)
        #self.cursor = self.conn.cursor()
        #yield self.cursor
        #self.conn.commit()
        #self.conn.close()
        #self.cursor.close()
        try:
            self.conn = connect(**self.config_dict)
            self.cursor = self.conn.cursor()
            yield self.cursor
        except psycopg2.DataError, e:
            print e
            self.cursor.close()
        except:
            self.cursor.close()
        finally:
            self.conn.commit()
            self.conn.close()

    def execute_query(self, sql_context, **data):
        with self.execute_base() as cur:
            cur.execute(sql_context, **data)
            result = cur.fetchall()
            return result

    def execute_push(self, sql_context, **data):
        print data
        with self.execute_base() as cur:
            cur.execute(sql_context, data)



def getToken(db, http, url): 
    sql_context = "select appid, appsecret from wechat_info limit 1;"
    result = db.execute_query(sql_context)
    appid, appsecret =  result[0]
    data = dict(grant_type='client_credential')
    data.update(dict(appid=appid, secret=appsecret))
    result = http.urlGet(url, **data)
    origin_data = result
    update_sql = "update wechat_info set token = %(access_token)s where appid = %(appid)s;"
    db.execute_push(update_sql, access_token=origin_data['access_token'], appid=appid)
    print origin_data['access_token']
    return origin_data['expires_in']


def getTimestamp(db):
    sql_context = "select timestamp from wechat_info limit 1;"
    time_data = db.execute_query(sql_context)
    return int(time.mktime(time_data[0][0].timetuple()))


def main():
    file_path = os.path.split(os.path.realpath(__file__))[0] + '/'
    config_file = file_path + 'conf.d/'
    config = parseParams(config_file)
    db_config = config['db']
    interval = 72000
    db = SyncPG(**db_config)
    older_time = getTimestamp(db)
    now_time = int(time.time())
    time_diff = now_time - older_time
    api = 'https://api.weixin.qq.com/cgi-bin/token'
    http = RequestUrl()
    while True:
        older_time = getTimestamp(db)
        if time_diff > interval:
            interval = getToken(db, http, api)
        else:
            time.sleep(time_diff - 1)



if __name__ == '__main__':
    main()
