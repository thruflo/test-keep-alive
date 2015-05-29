
import gevent
import json
import os
import time

settings = {
    'interval': int(os.environ.get('INTERVAL', 5)),
    'timeout': int(os.environ.get('TIMEOUT', 65)),
    'use_empty_strings': bool(os.environ.get('USE_EMPTY_STRINGS', False)),
}

def stream():
    delay = settings['interval']
    deadline = time.time() + settings['timeout']
    message = '' if settings['use_empty_strings'] else '\0'
    while True:
        if time.time() > deadline:
            break
        # msg = message.format(delay)
        print message
        yield message
        gevent.sleep(delay)
    payload = json.dumps({'status': u'Done'})
    print payload
    yield payload

def app(environ, start_response):
    headers = [
        ("Content-Type", "text/plain"),
        ("Connection", "Keep-Alive"),
    ]
    print headers
    start_response("200 OK", headers=headers)
    return stream()
