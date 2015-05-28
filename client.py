#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='https://test-keep-alive.herokuapp.com')
    parser.add_argument('--stream', dest='should_stream', action='store_true')
    parser.add_argument('--no-stream', dest='should_stream', action='store_false')
    parser.set_defaults(should_stream=True)
    return parser.parse_args()

def main(host, should_stream):
    if should_stream:
        r = requests.get(host, stream=True)
        try:
            for line in r.iter_lines():
                print line
        finally:
            r.close()
    else:
        r = requests.get(args.host)
        print r.text

if __name__ == '__main__':
    args = parse_args()
    try:
        main(args.host, args.should_stream)
    except KeyboardInterrupt:
        pass
