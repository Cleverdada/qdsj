#!/usr/bin/python
# encoding:utf-8

import os
root_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

log_path = os.path.join(root_path, "log")
cache_path = os.path.join(root_path, "cache")

conf_file = os.path.join(root_path, "conf", "connect.conf")
log_file = os.path.join(root_path, "util", "logging.conf")

pre_make = [log_path, cache_path]

for pm in pre_make:
    if not os.path.exists(pm):
        os.makedirs(pm)