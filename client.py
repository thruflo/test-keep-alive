#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import requests

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='https://test-keep-alive.herokuapp.com')
    parser.add_argument('--stream', dest='should_stream', action='store_true')
    parser.add_argument('--no-stream', dest='should_stream', action='store_false')
    parser.set_defaults(should_stream=True)
    return parser.parse_args()

def stream(host):
    r = requests.get(host, stream=True)
    try:
        for item in r.iter_content():
            print item
    finally:
        r.close()

def fetch(host):
    r = requests.get(args.host)
    print r.status_code, r.text

if __name__ == '__main__':
    args = parse_args()
    request = stream if args.should_stream else fetch
    try:
        request(args.host)
    except KeyboardInterrupt:
        pass
