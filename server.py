
import gevent
import os

settings = {
    'max_delay': int(os.environ.get('MAX_DELAY', 120)),
    'use_empty_strings': bool(os.environ.get('USE_EMPTY_STRINGS', False)),
}

def stream():
    i = 0
    message = '' if settings['use_empty_strings'] else '{0}\r\n'
    while i < settings['max_delay']:
        i = i + 2
        gevent.sleep(i)
        yield message.format(i)
    yield '\r\n'
    yield 'Done!'

def app(environ, start_response):
    headers = [
        ("Content-Type", "text/plain"),
    ]
    if environ.get('HTTP_CONNECTION') == 'keep-alive':
        headers.append(("Connection", "Keep-Alive"))
    print headers
    start_response("200 OK", headers=headers)
    return stream()
