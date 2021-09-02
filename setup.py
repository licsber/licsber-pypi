#!/usr/bin/env python
# coding: utf-8

import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='licsber',
    version='4.4.4',
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
        'tqdm',
    ],
    extras_require={
        'all': [
            'opencv-python',
            'paddlepaddle~=2.0',
            'beautifulsoup4',
            'pycryptodome',
            'minio',
            'h5py',
            'matplotlib',
        ],
        'cv': [
            'opencv-python',
            'matplotlib',
        ],
        'wisedu': [
            'opencv-python',
            'pycryptodome',
            'beautifulsoup4',
            'paddlepaddle~=2.0',
        ],
        'datasets': [
            'h5py',
        ],
        's3': [
            'minio',
        ],
    },
    entry_points={
        'console_scripts': [
            'licsber=licsber.shell.hello:licsber',
            'count-dir=licsber.shell.dir_ops:count_dir',
            'flatten-dir=licsber.shell.dir_ops:flatten_dir',
            'empty-dir=licsber.shell.dir_ops:empty_dir',
            'rename=licsber.shell.dir_ops:rename',
            'save-115-dir=licsber.shell.cloud_drive:save_115_dir',
            'conv=licsber.shell.cloud_drive:conv',
            'memobird=licsber.shell:memobird',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
    ],
    license='GPLv3',
)
