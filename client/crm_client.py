#!/usr/bin/python
# encoding:utf-8
import StringIO
import gzip
import json
import os
import time
import urllib

import requests

import util.dynamic as dynamic
from util.logger import trace
from util.tools import Encoder
from util.logger import info
from exception.BaseError import ServerError

CONNECT_TIMEOUT = 100
READ_TIMEOUT = 5 * 60
VERSION = "1.0.0"
# HEADERS = {
#     'Content-type': 'application/json;charset=utf-8',
#     'Content-Encoding': 'gzip',
#     'User-Agent': 'SyncForCRM/%s-%s' % (VERSION, os.name)
# }

HEADERS = {
    'Content-type': 'application/json;charset=utf-8',
    'User-Agent': 'SyncForCRM/%s-%s' % (VERSION, os.name)
}

timeout = (CONNECT_TIMEOUT, READ_TIMEOUT)


def catch_httpfailed(func):
    def _func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.ConnectionError, e:
            trace(e)
            raise Exception(u"网络连接不可用，无法连接到服务端，请检查您的网络配置。")

    return _func


class HttpClient(object):
    """
    OpenDS交互模块
    """
    def __init__(self):
        self.url_prefix = dynamic.get("out", "url")
        requests.packages.urllib3.disable_warnings()

    @catch_httpfailed
    def _request(self, url, payload=None, param=None):
        if not payload:
            payload = {}
        if not param:
            param = {}
        param['_t'] = time.time()
        try_count = 0
        start = time.time()
        while True:
            try:
                params = '%s' % urllib.urlencode(param)
                _url = "%s?%s" % (url, params)
                if payload:
                    payload_str = u'%s' % json.dumps(payload, cls=Encoder)
                    # gzip
                    # s = StringIO.StringIO()
                    # data = gzip.GzipFile(fileobj=s, mode='w')
                    # data.write(payload_str)
                    # data.close()
                    # zip_value = s.getvalue()
                    start_request = time.time()
                    res = requests.post(_url, data=payload_str, headers=HEADERS, verify=False, timeout=timeout)
                else:
                    start_request = time.time()
                    res = requests.get(_url, headers=HEADERS, verify=False, timeout=timeout)
                if res.status_code != 200:
                    raise Exception(res.status_code, 'url: %s, http: %s -> %s' % (url, res.status_code, res.text))
                result = json.loads(res.text)
                info().info(json.dumps(result, indent=2))
                break
            except requests.RequestException, e:
                try_count += 1
                info().info(u'can not connect to server, retry ... | reason: %s' % str(e))
                time.sleep(5)
                if try_count == 1:
                    raise

        info().info(u'api:%s\t request_id:%s\t request_cost:%.5ss, http:%.5ss' % (
            '/'.join(url.split('/')[-2:]),
            result.get('request_id', ''),
            time.time() - start,
            time.time() - start_request
        ))

        if result['status'] != 0:
            message = '{errstr} {request_id}'.format(**result)
            raise ServerError(result['status'], message)
        return result.get('result')

    def tb_max_id(self, ds_name, tb_name):
        url = '%s/api/tb/max_id' % self.url_prefix
        param = {
            'ds_name': ds_name,
            'tb_name': tb_name,
        }
        return self._request(url, param=param)

    def tb_push(self, ds_name, tb_name, fields, data, extra_field):
        if not len(data):
            return
        url = '%s/api/tb/push' % self.url_prefix
        payload = {
            'ds_name': ds_name,
            'tb_name': tb_name,
            'fields': fields,
            'data': data,
            'extra_field': extra_field
        }
        return self._request(url, payload=payload)