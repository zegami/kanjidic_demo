# Copyright 2017 Zegami Ltd

"""Tools for making http requests."""

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


def download(url, filename):
    """Fetch url and write into filename."""
    response = urlopen(url)
    try:
        _pump_to_file(response, filename)
    finally:
        response.close()


def _pump_to_file(source, filename, _chunk_size=(1 << 15)):
    with open(filename, "wb") as f:
        while True:
            data = source.read(_chunk_size)
            if not data:
                break
            f.write(data)
