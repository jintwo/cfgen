#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import codecs
import warnings
from os import path

from pyrsistent import pmap

from .utils import walk, env, subst
from .renderer import get_renderer
from .parser import get_parser


def _create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('settings', help='Settings file.')
    parser.add_argument('profile', help='Profile name.')
    parser.add_argument(
        '-t', '--templates', help='Templates dir.', default='templates')
    parser.add_argument(
        '-o', '--output', help='Output dir.', default='output')
    parser.add_argument(
        '-p',
        '--parser',
        help='Config parser type.',
        default='json',
        choices=['json', 'yaml'])
    parser.add_argument(
        '-r',
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


def _eval_val(val, params):
    return env(subst(val, params))


def _eval_params(params):
    return walk(params, lambda val: _eval_val(val, params))


def _render(renderer, template_name, params):
    return renderer.render_template(template_name, _eval_params(params))


def _get_params(profiles_dict, profile_name):
    return pmap().update(profiles_dict.get('_', {}))\
                 .update(profiles_dict.get(profile_name, {}))


def main():
    args = _create_arg_parser().parse_args()
    config = _parse_config(args.parser, args.settings)
    renderer = _prepare_renderer(args.renderer, args.templates)

    profiles = pmap(config.get('profiles', {}))
    templates = pmap(config.get('templates', {}))

    for template_name, data in templates.items():
        template_profiles = data.get('profiles', {})

        if (
            args.profile not in profiles and
            args.profile not in template_profiles
        ):
            warnings.warn(
                'Profile <{}> not found for <{}>'.format(
                    args.profile, template_name))

        output_filename = data.get('output', template_name)
        if not output_filename:
            raise Exception('Invalid output file name.')

        params = pmap().update(_get_params(profiles, args.profile))\
                       .update(_get_params(template_profiles, args.profile))\
                       .update({'profile': args.profile})
        output_data = _render(renderer, template_name, params)
        output_filename = _eval_val(output_filename, params)
        output_path = path.join(args.output, output_filename)
        with codecs.open(output_path, 'w', 'utf8') as output_file:
            output_file.write(output_data)


if __name__ == '__main__':
    main()
