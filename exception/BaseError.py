#!/usr/bin/python
# encoding:utf-8


class BaseError(Exception):
    """
        所有已知异常
    """

    def __init__(self, status, err_msg):
        self.status_code = status
        self.err_msg = err_msg

    def __repr__(self):
        return 'StatusCode: %s, Message: %s' % (self.status_code, self.err_msg)

    def __str__(self):
        return self.__repr__()


class ServerError(BaseError):
    """
        服务端抛出的异常
    """

    def __init__(self, status, err_msg):
        self.status_code = status
        self.err_msg = err_msg

    def __repr__(self):
        return 'ServerError, StatusCode: %s, Message: %s' % (self.status_code, self.err_msg)

    def __str__(self):
        return self.__repr__()


class ClientError(BaseError):
    """
        客户端抛出的异常
    """

    def __init__(self, status, err_msg):
        self.status_code = status
        self.err_msg = err_msg

    def __repr__(self):
        return 'ClientError, StatusCode: %s, Message: %s' % (self.status_code, self.err_msg)

    def __str__(self):
        return self.__repr__()