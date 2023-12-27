#!/usr/bin/env python3

from setuptools import setup

setup(
    name='epyjson',
    description='Python library for processing e-JSON',
    version='0.0.1',
    author='Dan Gordon',
    author_email='dan.gordon@anu.edu.au',
    packages=['epyjson'],
    install_requires = [
        'jsonschema',
        'numpy',
        'networkx',
        'ordered-set',
    ],
    scripts=[
    ],
    package_data={'epyjson': ['e-json-schema.json']}
)
