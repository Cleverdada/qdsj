#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import static
import util.dynamic as dynamic
import util.mysql as db_helper
import util.yaml_util as yaml_util
from client.crm_client import HttpClient
from exception.BaseError import BaseError
from util.logger import info, trace


class SyncCRM(object):
    connection = db_helper.connect()
    db = dynamic.get_section("connect_info").get("db")
    tables = dynamic.get_section("sync_info").get("tables").split(",")
    http_client = HttpClient()

    def sync_tbs(self):
        for table in self.tables:
            self.sync_tb(table)

    def sync_tb(self, table_name):
        table_path = os.path.join(static.cache_path, "%s.yaml" % table_name)
        table_info = yaml_util.load(table_path)
        info().info(table_info)

        self.get_max_id(table_info, table_path, self.db)
        data = self.fetch_data(table_info)

        field_names = [field.get("field_name") for field in table_info.get("fields")]
        extra_field = table_info.get("extra_field")
        self.push_data(self.db, table_name, field_names, data, extra_field)
        while data:
            self.get_max_id(table_info, table_path, self.db)
            data = self.fetch_data(table_info)
            self.push_data(self.db, table_name, data, field_names, extra_field)

    def get_max_id(self, table_info, table_path, db_name):
        tb_name = table_info.get("table_name")
        max_id = self.http_client.tb_max_id(db_name, tb_name).get("max_id")
        table_info.update({"increase_value": max_id})
        yaml_util.dump(table_info, table_path)
        info().info(u"max id change to %s" % max_id)
        return

    def push_data(self, db_name, tb_name, field_names, data, extra_field):
        self.http_client.tb_push(db_name, tb_name, field_names, data, extra_field)

    def fetch_data(self, table_info):
        cursor = db_helper.create_cursor(self.connection)
        tb_name = table_info.get("table_name")
        fields = table_info.get("fields")
        sql = u"select %s from %s %s" % (self.field_join(fields), tb_name, self.where_condition(table_info))
        info().info(sql)
        cursor.execute("use `%s`;" % self.db)
        cursor.execute(sql)
        data = cursor.fetchmany(table_info.get("size"))
        info().info(u"fetched %s datas" % len(data))
        if cursor:
            cursor.close()
        return data

    def field_join(self, fields):
        decor_field_names = map(lambda field: self.wrap_field(field), fields)
        return ",".join(decor_field_names)

    def wrap_field(self, field):
        field_type = field.get("field_type")
        field_name = field.get("field_name")
        if field_type in ('datetime', 'date'):
            return u'cast(`%s` as datetime)' % (field_name)
        else:
            return u'`%s`' % (field_name)

    def where_condition(self, table_info):
        increase_field = table_info.get("increase_field")
        increase_value = table_info.get("increase_value")
        return "where `%s` > %s" % (increase_field, increase_value)


if __name__ == '__main__':
    try:
        SyncCRM().sync_tbs()
    except BaseError, be:
        trace(be.err_msg)
    except Exception, e:
        trace("unknown exception")
