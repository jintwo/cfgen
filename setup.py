#!/usr/bin/env python
from setuptools import setup, find_packages

import cfgen


setup(
    name='CFGen',
    author='Eugeny Volobuev',
    author_email='qulert@gmail.com',
    version=cfgen.__version__,
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
