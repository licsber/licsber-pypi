#!/bin/zsh

rm -rf dist/*
python setup.py sdist
python -m pip install dist/*
#python -m pip install --force-reinstall dist/*
conv /tmp/test/115_links.txt