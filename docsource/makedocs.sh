#!/bin/bash

find ../docs -mindepth 1 -delete
find ./build -mindepth 1 -delete
sphinx-build -b html source build
cp -r ./build/* ../docs/
touch ../docs/.nojekyll
chmod -R 777 ../docs/
find ./build -mindepth 1 -delete