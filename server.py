
import gevent
import json
import os
import time

ACK = '\0'
INTERVAL = int(os.environ.get('INTERVAL', 15))
TIMEOUT = int(os.environ.get('TIMEOUT', 80))

def stream():
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
    headers = [
        ("Content-Type", "text/plain"),
        ("Connection", "Keep-Alive"),
    ]
    print headers
    start_response("200 OK", headers=headers)
    return stream()
