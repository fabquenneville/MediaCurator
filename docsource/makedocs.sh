#!/bin/bash

find ../docs -mindepth 1 -delete
find ./build -mindepth 1 -delete
sphinx-build -b html source build
cp -r ./build/* ../docs/
chmod -R 777 ../docs/
touch ../docs/.nojekyll
find ./build -mindepth 1 -delete