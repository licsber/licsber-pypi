#!/bin/zsh

rm -rf dist/*
python setup.py sdist
python -m pip install dist/*
