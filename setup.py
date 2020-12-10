#!/usr/bin/env python3.6

from distutils.core import setup

setup(
    name='Resty',
    version='0.9',
    description='Generic REST client library',
    author='Sebastiaan Hoogeveen',
    packages=['resty'],
    install_requires=[
      're',
      'urllib',
      'base64',
      'json',
      'xml.etree'
    ]
)
