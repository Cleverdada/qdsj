#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import static
import util.dynamic as dynamic
import util.mysql as db_helper
import util.yaml_util as yaml_util
from util.logger import info, trace
from exception.BaseError import BaseError


class GenSchema(object):
    connection = db_helper.connect()
    db = dynamic.get_section("connect_info").get("db")
    tables = dynamic.get_section("sync_info").get("tables").split(",")

    def gen_tb(self, table_name):
        FD_NAME = 0
        FD_TYPE = 1
        table_path = os.path.join(static.cache_path, "%s.yaml" % table_name)
        if os.path.exists(table_path):
            info().info(u"conf file %s has exists," % table_path)
            return
        # get tb_info
        tb_info = self.fetch_schema(self.db, table_name)
        table = {
            "table_name": table_name,
            "fields": [],
            "increase_field": "id",
            "increase_value": 0,
            "extra_field": "",
            "size": 20000,
        }
        fields = table.get("fields")
        for fd in tb_info:
            field = {"field_name": fd[FD_NAME],
                     "field_type": fd[FD_TYPE]}
            fields.append(field)
        table.update({"fields": fields})
        yaml_util.dump(table, table_path)

    def fetch_schema(self, db_name, tb_name):
        cursor = db_helper.create_cursor(self.connection)
        sql = "SELECT `COLUMN_NAME`,`DATA_TYPE`" \
              "FROM information_schema.columns " \
              "where TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s' " % (db_name, tb_name)
        cursor.execute(sql)
        data = cursor.fetchall()
        if cursor:
            cursor.close()
        return data

    def gen_tbs(self):
        for table in self.tables:
            self.gen_tb(table)


if __name__ == '__main__':
    try:
        GenSchema().gen_tbs()
    except BaseError, be:
        trace(be.err_msg)
    except Exception, e:
        trace("unknown exception")
