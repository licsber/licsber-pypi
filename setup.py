#!/usr/bin/env python
# coding: utf-8

import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='licsber',
    version='3.1.0',
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
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'licsber=licsber.shell.hello:licsber',
            'memobird=licsber.shell:memobird',
            'count-dir=licsber.shell.dir_ops:count_dir',
            'flatten-dir=licsber.shell.dir_ops:flatten_dir',
            'empty-dir=licsber.shell.dir_ops:empty_dir',
            'archive=licsber.shell.dir_ops:archive',
            'rename=licsber.shell.dir_ops:rename',
            'save-115=licsber.shell.cloud_drive:save_115_link',
            'conv=licsber.shell.cloud_drive:conv',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
    ],
    license='GPLv3',
)
