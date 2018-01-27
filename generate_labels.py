#!/usr/bin/env python3.6
import argparse
import itertools
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


def _req(*, url, data, token, method='POST'):
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header('Authorization', f'token {token}')
    urllib.request.urlopen(request)
    # https://developer.github.com/v3/guides/best-practices-for-integrators/#dealing-with-abuse-rate-limits
    time.sleep(1)


def _label(color, *, token, repo):
    url = f'https://api.github.com/repos/{repo}/labels'
    data = json.dumps({'name': color, 'color': color}).encode()
    _req(url=url, data=data, token=token)


def _create_labels(*, repo, dry_run):
    for color in colors():
        print(f'Creating {color}')
        if not dry_run:
            _label(color, token=os.environ['GH_TOKEN'], repo=repo)


def _assign_some_labels(labels, *, token, repo, issue):
    url = f'https://api.github.com/repos/{repo}/issues/{issue}/labels'
    data = json.dumps(labels).encode()
    _req(url=url, data=data, token=token)


def _assign_labels(*, repo, issue):
    token = os.environ['GH_TOKEN']
    all_colors = colors()
    next_labels = tuple(itertools.islice(all_colors, 0, 100))
    while next_labels:
        _assign_some_labels(next_labels, token=token, repo=repo, issue=issue)
        next_labels = tuple(itertools.islice(all_colors, 0, 100))


def _unassign_labels(*, repo, issue):
    token = os.environ['GH_TOKEN']
    url = f'https://api.github.com/repos/{repo}/issues/{issue}/labels'
    data = b'[]'
    _req(url=url, data=data, token=token, method='PUT')


def main(argv=None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    create_labels = subparsers.add_parser('create-labels')
    create_labels.add_argument('--repo', default='asottile/label-test')
    create_labels.add_argument('--dry-run', action='store_true')

    for cmd in ('assign-labels', 'unassign-labels'):
        subp = subparsers.add_parser(cmd)
        subp.add_argument('--repo', default='asottile/label-test')
        subp.add_argument('--issue', default='1')

    args = parser.parse_args(argv)

    if args.command == 'create-labels':
        return _create_labels(repo=args.repo, dry_run=args.dry_run)
    elif args.command == 'assign-labels':
        return _assign_labels(repo=args.repo, issue=args.issue)
    elif args.command == 'unassign-labels':
        return _unassign_labels(repo=args.repo, issue=args.issue)
    else:
        raise NotImplementedError(args.command)


if __name__ == '__main__':
    exit(main())
