#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import codecs
import warnings
from os import path


from .utils import walk, env, subst
from .renderer import get_renderer
from .parser import get_parser


def _create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('settings', help='Settings file.')
    parser.add_argument('profile', help='Profile name.')
    parser.add_argument(
        '-t', '--templates', help='Templates root.', default='.')
    parser.add_argument(
        '-o', '--output', help='Output path.', default='.')
    parser.add_argument(
        '--parser',
        help='Config parser type.',
        default='json',
        choices=['json', 'yaml'])
    parser.add_argument(
        '--renderer',
        help='Template renderer type.',
        default='jinja2',
        choices=['jinja2'])
    return parser


def _parse_config(parser_type, config_filename):
    parser_cls = get_parser(parser_type)
    parser = parser_cls()
    return parser.parse_file(config_filename)


def _prepare_renderer(renderer_type, templates_path):
    renderer_cls = get_renderer(renderer_type)
    return renderer_cls(templates_path)


def _render(renderer, template_name, data):
    return renderer.render_template(
        template_name,
        walk(data, lambda val: env(subst(val, data))))


def _get_base_params(defaults, data):
    base_params = defaults.copy()
    base_params.update(data.get('defaults', {}))
    return base_params


def main():
    args = _create_arg_parser().parse_args()
    config = _parse_config(args.parser, args.settings)
    renderer = _prepare_renderer(args.renderer, args.templates)
    defaults = config.pop('defaults', {})

    for template_name, data in config.items():
        output_filename = data.get('output', template_name)
        if not output_filename:
            raise Exception('Invalid output file name.')

        profiles = data.get('profiles', {})
        if args.profile not in profiles:
            warnings.warn(
                'Profile <{}> not found for <{}>'.format(
                    args.profile, template_name))

        profile_data = profiles.get(args.profile, {})
        template_params = _get_base_params(defaults, data)
        template_params['profile'] = args.profile
        template_params.update(profile_data)

        output_data = _render(renderer, template_name, template_params)
        output_path = path.join(args.output, output_filename)
        with codecs.open(output_path, 'w', 'utf8') as output_file:
            output_file.write(output_data)


if __name__ == '__main__':
    main()
