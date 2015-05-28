import requests
import sys

def consume(r):
    for line in r.iter_lines():
        print line

if __name__ == '__main__':
    r = requests.get('https://test-keep-alive.herokuapp.com', stream=True)
    try:
        consume(r)
    except (KeyboardInterrupt, StopIteration):
        pass
    r.close()
