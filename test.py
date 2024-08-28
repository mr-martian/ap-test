#!/usr/bin/env python3

import subprocess
import os
import os.path
import shutil

def get_required(name):
    if name.count('-') == 2:
        _, l1, l2 = name.split('-')
        return [f'apertium-{l1}', f'apertium-{l2}']
    return []

def update_lang(name):
    if not os.path.isdir(name):
        subprocess.run(['git', 'clone', '--depth', '1',
                        f'https://github.com/apertium/{name}'])
        args = ['./autogen.sh']
        for n, req in enumerate(get_required(name), 1):
            args.append(f'--with-lang{n}=../{req}')
        subprocess.run(args, cwd=name)
    else:
        subprocess.run(['git', 'fetch', '--all', '--depth', '1'], cwd=name)
        subprocess.run(['git', 'reset', '--hard', 'origin/master'], cwd=name)
        subprocess.run(['make', 'clean'], cwd=name)
    subprocess.run(['make', '-j4'], cwd=name)

def update_all_langs(needed):
    todo = sorted(needed)
    done = set()
    while todo:
        cur = todo.pop()
        if cur in done:
            continue
        req = get_required(cur)
        if all(r in done for r in req):
            update_lang(cur)
            done.add(cur)
        else:
            todo.append(cur)
            todo += req

def build_tools(ltbranch, apbranch):
    if not os.path.isdir('lttoolbox'):
        subprocess.run(['git', 'clone', 'https://github.com/apertium/lttoolbox'])
    if not os.path.isdir('apertium'):
        subprocess.run(['git', 'clone', 'https://github.com/apertium/apertium'])
    subprocess.run(['test/rebuild-tools.sh', ltbranch, apbranch])

def run_test(modes, ltbranch, apbranch):
    build_tools(ltbranch, apbranch)
    update_all_langs(set(m['dir'] for m in modes.values()))
    for m in sorted(modes):
        d = modes[m]['dir']
        i = modes[m]['input']
        prefix = f'test/output/{m}.{ltbranch}.{apbranch}'
        with open(f'{prefix}.err.txt', 'w') as ferr:
            subprocess.run(['apertium', '-d', os.path.join('langs', d),
                            m, i, f'{prefix}.out.txt'], stderr=ferr)

def run_both(modes, ltbranch, apbranch):
    if os.path.isdir('test/output'):
        shutil.rmtree('test/output')
    os.mkdir('test/output')
    run_test(modes, 'main', 'main')
    run_test(modes, ltbranch, apbranch)

if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument('config', action='store')
    parser.add_argument('ltbranch', action='store')
    parser.add_argument('apbranch', action='store')
    args = parser.parse_args()
    with open(args.config) as fin:
        modes = json.load(fin)
    run_both(modes, args.ltbranch, args.apbranch)
