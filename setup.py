#!/usr/bin/env python

# Copyright 2018 Red Hat Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# Version reading from yacfg/meta.py
# according to (3b) from:
# https://packaging.python.org/guides/single-sourcing-package-version/
meta = {}
meta_file = path.join(this_directory, 'src/yacfg/meta.py')
with open(meta_file, encoding='utf-8') as meta_file:
    exec(meta_file.read(), meta)

setup(
    name="yacfg",
    version='0.9.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'yacfg = yacfg.yacfg_cli:main',
            'yacfg-batch = yacfg_batch.yacfg_batch_cli:main'
        ],
    },
    install_requires=[
        'jinja2==2.11.3',
        'pyyaml==20.4.0',
    ],
    extras_require={
        'color_log': ['colorlog>=5.0.1,<6.0.0', 'colorama>=0.4.4,<0.5.0']
    },
    url='https://github.com/rh-messaging-qe/yacfg',
    license='Apache-2.0',
    author='Zdenek Kraus',
    author_email='zkraus@redhat.com',
    maintainer='Dominik Lenoch',
    maintainer_email='dlenoch@redhat.com',
    description= "Template based configuration files generator based on jinja2 and yaml.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ],
)
