#!/usr/bin/python
# encoding:utf-8

import logging
import logging.config
import static
from traceback import format_exc

logging.config.fileConfig(static.log_file, defaults={"log_path": static.log_path})


def info():
    return logging.getLogger('root')


def error():
    return logging.getLogger('error')


def warn():
    return logging.getLogger('warning')


def perform():
    return logging.getLogger('performance')


def trace(message):
    error().error(format_exc().decode("utf-8"))
    info().error(unicode(message))


def debug(message):
    info().debug(message)


def runtime(msg):
    info().info(msg)
