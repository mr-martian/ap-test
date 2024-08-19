#!/bin/bash

ltbranch=$1
apbranch=$2

pushd lttoolbox
git fetch --all
git reset --hard "origin/$ltbranch"
autoreconf -fvi
./configure
make clean
make -j4
popd

pushd apertium
git fetch --all
git reset --hard "origin/$apbranch"
autoreconf -fvi
./configure
make clean
make -j4
popd
