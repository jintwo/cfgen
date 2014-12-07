# -*- coding: utf-8 -*-
from os import getenv
import re


def walk(dict_, fn=lambda value: value):
    result = {}
    for key, value in dict_.iteritems():
        if isinstance(value, dict):
            result[key] = walk(value, fn)
        elif isinstance(value, list):
            result[key] = map(fn, value)
        else:
            result[key] = fn(value)
    return result


def env(value):
    if not isinstance(value, basestring):
        return value
    result = value
    matches = re.findall(r'\$\(.*?\)', result)
    if matches:
        for m in matches:
            result = result.replace(m, getenv(m[2:-1], ''))
    return result


def subst(value, environ):
    if not isinstance(value, basestring):
        return value
    result = value
    matches = re.findall(r'\$\{.*?\}', result)
    if matches:
        for m in matches:
            var_name = m[2:-1]
            result = result.replace(m, environ.get(var_name))
    return result


# def include(value):
#     if not isinstance(value, basestring):
#         return value
#     result = value
#     if value.startswith('$include(') and value.endswith(')'):
#         filename = result.replace('$include(', '')[:-1]
#         result = json.loads(open(filename, 'r').read())
#     return result
