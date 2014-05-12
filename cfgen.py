#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import codecs
import json
from os import path, getenv
import re
import warnings

from jinja2 import Environment, FileSystemLoader


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


def include(value):
    if not isinstance(value, basestring):
        return value
    result = value
    if value.startswith('$include(') and value.endswith(')'):
        filename = result.replace('$include(', '')[:-1]
        result = json.loads(open(filename, 'r').read())
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('settings', help='Settings file')
    parser.add_argument('profile', help='Profile name')
    parser.add_argument(
        '-t', '--templates', help='Templates root', default='.')
    parser.add_argument(
        '-o', '--output', help='Output path', default='.')
    args = parser.parse_args()
    jinja_env = Environment(loader=FileSystemLoader(args.templates))
    config = json.loads(open(args.settings, 'r').read())
    defaults = config.pop('defaults', {})

    for template_name, data in config.items():
        template = jinja_env.get_template(template_name)

        output_file_name = data.get('output', template_name)
        if not output_file_name:
            raise Exception('Invalid output file name.')

        profiles = data.get('profiles', {}).copy()
        if args.profile not in profiles:
            warnings.warn('Profile <{}> not found for <{}>'.format(
                args.profile, template_name))

        profile_params = profiles.get(args.profile, {})

        template_params = dict(
            defaults.items() +
            data.get('defaults', {}).items()
        )
        template_params['profile'] = args.profile
        template_params.update(profile_params)
        template_params = walk(template_params,
                               lambda val: env(subst(include(val),
                                                     template_params)))
        output_data = template.render(**template_params)
        output_file_path = path.join(args.output, output_file_name)
        with codecs.open(output_file_path, 'w', 'utf8') as output_file:
            output_file.write(output_data)

if __name__ == '__main__':
    main()
