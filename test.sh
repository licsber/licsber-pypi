#!/usr/bin/env zsh

rm -rf dist/*
python setup.py sdist
python -m pip install dist/*
#python -m pip install --force-reinstall dist/*
