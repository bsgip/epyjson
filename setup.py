#!/usr/bin/env python3

from setuptools import setup

setup(
    name='epyjson',
    version='0.0.1',
    author='Dan Gordon, Anna Skobeleva',
    author_email='dan.gordon@anu.edu.au, anna.skobeleva@anu.edu.au',
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
