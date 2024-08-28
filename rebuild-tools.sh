#!/bin/bash

ltbranch=$1
apbranch=$2

pushd lttoolbox
git fetch --all --depth 1
git reset --hard "origin/$ltbranch"
./autogen.sh
make clean
make -j4
make install
popd

pushd apertium
git fetch --all --depth 1
git reset --hard "origin/$apbranch"
./autogen.sh
make clean
make -j4
make install
popd
