#!/usr/bin/env python3

import argparse
import json
parser = argparse.ArgumentParser()
parser.add_argument('config', action='store')
parser.add_argument('ltbranch', action='store')
parser.add_argument('apbranch', action='store')
args = parser.parse_args()
with open(args.config) as fin:
    modes = json.load(fin)

print(f'''#!/bin/bash

git clone https://github.com/apertium/lttoolbox --depth 1
pushd lttoolbox
git fetch --all --depth 1
git reset --hard "origin/{args.ltbranch}"
./autogen.sh
make clean
make -j4
make install
popd

git clone https://github.com/apertium/apertium --depth 1
pushd apertium
git fetch --all --depth 1
git reset --hard "origin/{args.apbranch}"
./autogen.sh
make clean
make -j4
make install
popd

''')

for package in sorted(set(m['dir'] for m in modes.values())):
    print('apertium-get', package.replace('apertium-', ''), '--depth 1')

print('')

for m, d in sorted(modes.items()):
    prefix = f'test/output/{m}.{args.ltbranch}.{args.apbranch}'
    print(f'apertium -d {d["dir"]} {m} "{d["input"]}" "{prefix}.out.txt" 2>"{prefix}.err.txt"')
