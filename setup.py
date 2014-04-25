#!/usr/bin/env python
from setuptools import setup

__VERSION__ = (0, 2, 8)

setup(
    name='CFGen',
    author='Eugeny Volobuev',
    author_email='qulert@gmail.com',
    version='.'.join(map(str, __VERSION__)),
    url='http://github.com/jintwo/cfgen',
    install_requires=['Jinja2>=2.6'],
    py_modules=['cfgen'],
    entry_points={
        'console_scripts': [
            'cfgen = cfgen:main'
        ]
    }
)
