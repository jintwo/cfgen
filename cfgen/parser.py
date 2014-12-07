# -*- coding: utf-8 -*-
import json
import warnings


def _get_parser_map():
    result = {'json': JSONConfigParser}
    try:
        import yaml
    except ImportError:
        warnings.warn('PyYAML not found.')
    else:
        result['yaml'] = YAMLConfigParser
    return result


def get_parser(config_type):
    parser_cls = __parser_map.get(config_type)
    if parser_cls is None:
        parser_cls = JSONConfigParser

    return parser_cls


class BaseConfigParser(object):
    def parse(self, buf):
        raise NotImplementedError()

    def parse_file(self, filename):
        with open(filename, 'r') as f:
            return self.parse(f.read())


class JSONConfigParser(BaseConfigParser):
    def parse(self, buf):
        return json.loads(buf)


class YAMLConfigParser(BaseConfigParser):
    def parse(self, buf):
        import yaml
        return yaml.load(buf)

__parser_map = _get_parser_map()
