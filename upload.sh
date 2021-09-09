#!/usr/bin/env zsh

rm -rf dist/*
python setup.py sdist
twine upload dist/*
