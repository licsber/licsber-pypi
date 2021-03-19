#!/usr/bin/env python
# coding: utf-8

import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='licsber',
    version='1.3.0',
    author='Licsber',
    author_email='licsber@gmail.com',
    url='https://www.cnblogs.com/licsber/',
    description=u'个人娱乐工具箱.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[
        'pymongo',
        'requests',
        'beautifulsoup4',
        'pycryptodome',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'licsber=licsber:licsber',
            'count-dir=licsber:count_dir',
            'flatten_dir=licsber:flatten_dir',
            'memobird=licsber:memobird',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
    ],
    license='GPLv3',
)
