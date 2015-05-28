
import gevent
import json
import os

settings = {
    'start_delay': int(os.environ.get('START_DELAY', 10)),
    'incr_delay': int(os.environ.get('INCR_DELAY', 10)),
    'max_delay': int(os.environ.get('MAX_DELAY', 120)),
    'use_empty_strings': bool(os.environ.get('USE_EMPTY_STRINGS', False)),
}

def stream():
    delay = 0 + settings['start_delay']
    message = '' if settings['use_empty_strings'] else '{0}\r\n'
    while delay < settings['max_delay']:
        yield message.format(delay)
        gevent.sleep(delay)
        delay = delay + settings['incr_delay']
    payload = json.dumps({'status': u'Done'})
    yield payload

def app(environ, start_response):
    headers = [
        ("Content-Type", "text/plain"),
    ]
    if environ.get('HTTP_CONNECTION') == 'keep-alive':
        headers.append(("Connection", "Keep-Alive"))
    print headers
    start_response("200 OK", headers=headers)
    return stream()
