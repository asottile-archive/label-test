#!/usr/bin/env python3.6
import argparse
import json
import os
import time
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
    # https://developer.github.com/v3/guides/best-practices-for-integrators/#dealing-with-abuse-rate-limits
    time.sleep(1)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', default='asottile/label-test')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)

    for color in colors():
        print(f'Creating {color}')
        if not args.dry_run:
            _label(color, token=os.environ['GH_TOKEN'], repo=args.repo)


if __name__ == '__main__':
    exit(main())
