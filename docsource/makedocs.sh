#!/bin/bash

find ../docs -mindepth 1 -delete
sphinx-build -b html source build
cp -r ./build/* ../docs/
find ./build -mindepth 1 -delete