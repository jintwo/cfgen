#!/usr/bin/env python
from setuptools import setup, find_packages
import cfgen

setup(
    name='CFGen',
    version='.'.join(map(str, cfgen.__VERSION__)),
    install_requires=['Jinja2>=2.6'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cfgen = cfgen:main'
        ]
    }
)
