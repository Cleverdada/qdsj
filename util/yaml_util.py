#!/usr/bin/python
# encoding:utf-8

import yaml


def load(fp):
    with open(fp, 'r') as f:
        return yaml.load(f)


def dump(data, fp):
    with open(fp, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False)
        # noalias_dumper = yaml.dumper.SafeDumper
        # noalias_dumper.ignore_aliases = lambda self, data: True
        # yaml.safe_dump(data, f, default_flow_style=False, Dumper=noalias_dumper)


if __name__ == '__main__':
    a = {
        "hehe": "hehe",
        "haha": u"haha",
        "shuzi": 1,
        "embed": {
            "field": "title"
        },
        "list": ["field", "field2"]
    }
    fp = "test.yaml"
    dump(a, fp)
