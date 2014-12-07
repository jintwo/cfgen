# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader, Template


class BaseRenderer(object):
    def __init__(self, templates_path):
        self.templates_path = templates_path

    def render(self, buf, data):
        raise NotImplementedError()

    def render_file(self, filename, data):
        with open(filename, 'r') as f:
            return self.render(f.read(), data)

    def render_template(self, template_name, data):
        raise NotImplementedError()


class JinjaRenderer(BaseRenderer):
    def __init__(self, templates_path):
        super(JinjaRenderer, self).__init__(templates_path)
        self.env = Environment(loader=FileSystemLoader(self.templates_path))

    def render(self, buf, data):
        return Template(buf).render(**data)

    def render_template(self, template_name, data):
        return self.env.get_template(template_name).render(**data)


def _get_renderer_map():
    return {'jinja': JinjaRenderer}


__renderer_map = _get_renderer_map()


def get_renderer(renderer_type):
    renderer_cls = __renderer_map.get(renderer_type)
    if renderer_cls is None:
        renderer_cls = JinjaRenderer

    return renderer_cls
