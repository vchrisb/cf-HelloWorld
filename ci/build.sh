#!/bin/bash

set -e -x


mkdir build-output/vendor
pip download -d build-output/vendor -r source-code/requirements.txt --no-binary :all:
cp -a source-code/{hello.py,runtime.txt,manifest.yml,requirements.txt,Procfile,templates} build-output/
pwd
ls -l build-output/
