#!/usr/bin/env python
# coding: utf-8

import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='licsber',
    version='2.1.0',
    author='Licsber',
    author_email='licsber@gmail.com',
    url='https://www.cnblogs.com/licsber/',
    description=u'个人娱乐工具箱.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'pymongo',
        'requests',
        'beautifulsoup4',
        'pycryptodome',
        'numpy',
        'minio',
        'matplotlib',
        'opencv-python',
        'h5py',
        'paddlepaddle~=2.1.0',
    ],
    entry_points={
        'console_scripts': [
            'licsber=licsber:licsber',
            'count-dir=licsber:count_dir',
            'flatten-dir=licsber:flatten_dir',
            'empty-dir=licsber:empty_dir',
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
