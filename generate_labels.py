#!/usr/bin/env python3.6
import argparse
import functools
import json
import multiprocessing.pool
import os
import urllib.request


def hexdigits():
    yield from range(0, 0xff, 16)
    yield 0xff


def colors():
    for r in hexdigits():
        for g in hexdigits():
            for b in hexdigits():
                yield f'{r:02x}{g:02x}{b:02x}'


def _label(color, *, token, repo):
    url = f'https://api.github.com/repos/{repo}/labels'
    data = json.dumps({'name': color, 'color': color}).encode()
    request = urllib.request.Request(url, data=data, method='POST')
    request.add_header('Authorization', f'token {token}')
    urllib.request.urlopen(request)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', default='asottile/label-test')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)

    if args.dry_run:
        mapper = map
        func = print
    else:
        token = os.environ['GH_TOKEN']
        mapper = multiprocessing.pool.ThreadPool(4).map
        func = functools.partial(_label, token=token, repo=args.repo)

    for _ in mapper(func, colors()):
        pass


if __name__ == '__main__':
    exit(main())
