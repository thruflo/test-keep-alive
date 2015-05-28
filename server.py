
import gevent

HEADERS = [
    ("Connection", "Keep-Alive"),
    ("Content-Type", "text/plain"),
]

def stream():
    i = 2
    while True:
        yield '{0}\r\n'.format(i)
        gevent.sleep(i)
        i = i + 2

def app(environ, start_response):
    start_response("200 OK", headers=HEADERS)
    return stream()
