#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import json
from os import path

from jinja2 import Environment, FileSystemLoader

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('settings', help='Settings file')
    parser.add_argument('profile', help='Profile name')
    parser.add_argument('-t', '--templates', help='Templates root', default='.')
    parser.add_argument('-o', '--output', help='Output path', default='.')
    args = parser.parse_args()
    env = Environment(loader=FileSystemLoader(args.templates))
    config = json.loads(open(args.settings, 'r').read())
    defaults = config.pop('defaults', {})

    for template_name, data in config.items():
        template = env.get_template(template_name)

        output_file_name = data.get('output')
        if not output_file_name:
            raise Exception('Invalid output file name.')

        profiles = data.get('profiles', {}).copy()
        if args.profile not in profiles:
            raise Exception('Invalid profile name')

        template_params = dict(
            defaults.items() +
            data.get('defaults', {}).items()
        )
        template_params.update(profiles[args.profile])

        output_data = template.render(**template_params)
        with open(path.join(args.output, output_file_name), 'w') as output_file:
            output_file.write(output_data)

if __name__ == '__main__':
    main()
