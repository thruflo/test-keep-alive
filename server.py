# -*- coding: utf-8 -*-

"""Example WSGI server that emits keep alives before returning a response."""

import gevent
import json
import os
import sys
import time

def is_true(value):
    return str(value) in map(str, [True, 1, 't', 'T'])

INTERVAL = int(os.environ.get('INTERVAL', 2))
TIMEOUT = int(os.environ.get('TIMEOUT', 5))
USE_EMPTY_STRING = is_true(os.environ.get('USE_EMPTY_STRING', False))
DELAY_HEADERS = is_true(os.environ.get('DELAY_HEADERS', False))
ACK = b'' if USE_EMPTY_STRING else b'\0'

if DELAY_HEADERS:
    import gunicorn.util as util
    import gunicorn.http.wsgi as wsgi
    orginal_write = wsgi.Response.write
    class PatchedResponse(wsgi.Response):
        def write(self, arg):
            if arg == ACK and not self.chunked:
                util.write(self.sock, arg, self.chunked)
            else:
                orginal_write(self, arg)
    wsgi.Response = PatchedResponse

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
    if DELAY_HEADERS:
        try: # wsgi requires a real exc_info
            raise Exception
        except Exception:
            status = '200 OK'
            headers = [('Content-Type', 'text/plain'),]
            print 'starting response', status, headers
            start_response(status, headers=headers, exc_info=sys.exc_info())
    payload = json.dumps({'status': u'Done'})
    yield payload

def app(environ, start_response):
    status = '204 No Content' if DELAY_HEADERS else '200 OK'
    print 'starting response', status
    start_response(status, headers=[])
    return handle(start_response)
