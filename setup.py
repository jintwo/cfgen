#!/usr/bin/env python
from setuptools import setup, find_packages

__VERSION__ = (0, 3, 0)

setup(
    name='CFGen',
    author='Eugeny Volobuev',
    author_email='qulert@gmail.com',
    version='.'.join(map(str, __VERSION__)),
    url='http://github.com/jintwo/cfgen',
    install_requires=['Jinja2>=2.6'],
    extras_require={
        'yaml_parser': ['PyYAML>=3.11']
    },
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cfgen = cfgen.cli:main'
        ]
    }
)
