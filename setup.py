# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup, find_namespace_packages


def readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except IOError:
        pass


setup(
    name='sphinxcontrib-luadomain',
    version='1.2.0',
    license='BSD-3-Clause',
    author='Eliott Dumeix',
    description='Sphinx domain for documenting Lua code',
    long_description=readme(),
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=['Sphinx>=4'],
)
