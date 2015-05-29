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
    parser.add_argument('--force-close', dest='force_close', action='store_true')
    parser.add_argument('--no-force-close', dest='force_close', action='store_false')
    parser.set_defaults(force_close=False)
    return parser.parse_args()

def main(host, should_stream, force_close):
    if should_stream:
        r = requests.get(host, stream=True)
        try:
            for line in r.iter_lines():
                print line
        finally:
            r.close()
    else:
        headers = {}
        if force_close:
            headers['Connection'] = 'Close'
        r = requests.get(args.host, headers=headers)
        print r.text
        try:
            print json.loads(r.text)
        except Exception:
            pass
    print r.status_code

if __name__ == '__main__':
    args = parse_args()
    try:
        main(args.host, args.should_stream, args.force_close)
    except KeyboardInterrupt:
        pass
