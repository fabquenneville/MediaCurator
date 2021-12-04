#!/bin/bash

source_path=$(readlink -f ../docs/)
docs_path=$(readlink -f ../docs/)
red='\033[0;31m'
cyan='\033[0;36m'
nc='\033[0m'

printf "${cyan}Cleaning${nc} docs and build directories.\n"
find ../docs -mindepth 1 -delete
find ./build -mindepth 1 -delete
printf "${cyan}Generating${nc} sphinx build.\n"
sphinx-build -b html source build
printf "${cyan}Prepping${nc} for release.\n"
cp -r ./build/* ../docs/
touch ../docs/.nojekyll
printf "${cyan}Cleaning${nc} up and setting proper permissions\n"
chmod -R 777 ../docs/
find ./build -mindepth 1 -delete
printf "Documentation ${cyan}ready for release${nc} in: ${red}${docs_path}${nc}\n"

