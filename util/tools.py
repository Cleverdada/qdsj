#!/usr/bin/python
# -*- coding: utf-8 -*-
import functools
import json
import math
import threading
from datetime import datetime, date, time as timeclass
from decimal import Decimal
from threading import Lock
from time import time, strptime, mktime, sleep
from uuid import uuid4

from util.logger import info


def byte_format(size, unit='Bytes'):
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    return ('%.2f' + " " + unit) % (size / math.pow(1024, units.index(unit)))


def bytearray_to_hex(bs):
    """Convert bytearray to hex string

    Given a bytearray, convert it to a string of
    an even length, containing the associated
    hexadecimal characters for each byte

    Args:
        bs:
    """
    try:
        hs = ["{0:0>2}".format(hex(b)[2:].upper()) for b in bs]
        return '0x' + ''.join(hs)
    except:
        return bs


def should_sync(timing, start):
    """

    Args:
        timing(list):
        start(datetime):
    """

    def datetime_to_stamp(string):
        """
        convert a datetime obj or a standard format datetime string to timestamp
        :param string:
        :return:
        """
        if not string:
            return None
        if isinstance(string, datetime):
            return mktime(string.timetuple())
        return mktime(strptime(str(string), '%Y-%m-%d %H:%M:%S'))

    if not timing:
        return False

    start_stamp = datetime_to_stamp(start)
    now_stamp = time()
    today = datetime.now().date()
    timestamps = map(lambda x: datetime_to_stamp('{date} {time}'.format(date=today, time=x)), timing)
    for timestamp in timestamps:
        if not start_stamp:
            return now_stamp > timestamp
        else:
            if start_stamp < timestamp <= now_stamp:
                return True

    return False


def retry(times=5, delay=5):
    """
    Retry a function call when has failed.
    Args:
        times:
        delay: how

    Returns:

    """
    assert isinstance(times, int)
    assert times >= 0
    assert isinstance(delay, (float, int))
    assert delay >= 0

    def _wrapper(func):

        @functools.wraps(func)
        def _inner(*args, **kwargs):

            retried = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception, e:
                    if retried >= times:
                        raise
                    sleep(delay)
                    retried += 1
                    info().info(
                        'Retry {retried}/{times} for function {func}, exception: {e}'.format(
                            retried=retried, times=times, func=func, e=e
                        )
                    )

        return _inner

    return _wrapper


def memory_cache():
    """
    a simple cache
    """
    pass


def utf8_len(s):
    """
    Return the length in utf8
    :param s:
    :return:
    """
    return len(s.encode('utf-8'))


def py_encode_basestring_ascii_improved(s):
    """Return an ASCII-only JSON representation of a Python string

    """
    if isinstance(s, str) and json.encoder.HAS_UTF8.search(s) is not None:
        try:
            s = s.decode('utf-8')
        except Exception:
            s = ''

    def replace(match):
        s = match.group(0)
        try:
            return json.encoder.ESCAPE_DCT[s]
        except KeyError:
            n = ord(s)
            if n < 0x10000:
                return '\\u{0:04x}'.format(n)
                # return '\\u%04x' % (n,)
            else:
                # surrogate pair
                n -= 0x10000
                s1 = 0xd800 | ((n >> 10) & 0x3ff)
                s2 = 0xdc00 | (n & 0x3ff)
                return '\\u{0:04x}\\u{1:04x}'.format(s1, s2)
                # return '\\u%04x\\u%04x' % (s1, s2)

    return '"' + str(json.encoder.ESCAPE_ASCII.sub(replace, s)) + '"'


json.encoder.encode_basestring_ascii = py_encode_basestring_ascii_improved


class Encoder(json.JSONEncoder):
    """
    Custom Json encode
    """

    def __init__(self, skipkeys=False, ensure_ascii=False, check_circular=True, allow_nan=True, sort_keys=False,
                 indent=None, separators=None, encoding='', default=None):

        super(Encoder, self).__init__(skipkeys, ensure_ascii, check_circular, allow_nan, sort_keys, indent, separators,
                                      encoding, default)

    def default(self, obj):
        if isinstance(obj, datetime):
            return '%04d-%02d-%02d %02d:%02d:%02d' % (obj.year, obj.month, obj.day, obj.hour, obj.minute, obj.second)
        if isinstance(obj, date):
            return '%04d-%02d-%02d 00:00:00' % (obj.year, obj.month, obj.day)
        if isinstance(obj, timeclass):
            return obj.strftime('%H:%M:%S')
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, threading.Thread):
            return obj.getName()
        else:
            return json.JSONEncoder.default(self, obj)


def timetrace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        print 'Execute function {func}, cost: {cost}'.format(func=func, cost=time() - start)
        return res

    return wrapper


method_lock = Lock()


def thread_safety(func):
    """
    Call a function thread safety
    :param func:
    :return:
    """

    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        with method_lock:
            return func(*args, **kwargs)

    return _wrapper


def uuid():
    """

    :return:
    """
    return str(uuid4())


if __name__ == '__main__':
    pass
