# -*- coding: utf-8 -*-

"""Example WSGI server that emits keep alives before returning a response."""

import gevent
import json
import os
import time

def is_true(value):
    return str(value) in map(str, [True, 1, 't', 'T'])

INTERVAL = int(os.environ.get('INTERVAL', 2))
TIMEOUT = int(os.environ.get('TIMEOUT', 3))
USE_EMPTY_STRING = is_true(os.environ.get('USE_EMPTY_STRING', False))
ACK = b'' if USE_EMPTY_STRING else b' '

def handle(start_response):
    t1 = time.time()
    ack_at = t1 + INTERVAL
    out_at = t1 + TIMEOUT
    while True:
        gevent.sleep(1)
        tn = time.time()
        if tn > out_at:
            break
        if tn < ack_at:
            continue
        ack_at = tn + INTERVAL
        yield ACK
    payload = json.dumps({'status': u'Done'})
    yield payload

def app(environ, start_response):
    start_response('200 OK', headers=[])
    return handle(start_response)
