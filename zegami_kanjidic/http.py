# Copyright 2017 Zegami Ltd

"""Tools for making http requests."""

import os

import requests


def download(session, url, filename):
    """Fetch url and write into filename."""
    with session.get(url, stream=True) as response:
        response.raise_for_status()
        _pump_to_file(response.raw, filename)


def _pump_to_file(source, filename, _chunk_size=(1 << 15)):
    with open(filename, "wb") as f:
        while True:
            data = source.read(_chunk_size)
            if not data:
                break
            f.write(data)


class TokenEndpointAuth(requests.auth.AuthBase):
    """Request auth that adds bearer token for specific endpoint only."""

    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token

    def __call__(self, request):
        if request.url.startswith(self.endpoint):
            request.headers["Authorization"] = "Bearer {}".format(self.token)
        return request


def make_session(auth=None):
    """Create a session object with optional auth handling."""
    session = requests.Session()
    session.auth = auth
    return session


def post_json(session, url, python_obj):
    """Send a json request and decode json response."""
    with session.post(url, json=python_obj) as response:
        response.raise_for_status()
        return response.json()


def post_file(session, url, filepath, mimetype):
    """Send a data file."""
    with open(filepath, 'rb') as f:
        details = (os.path.basename(filepath), f, mimetype)
        with session.post(url, files={'file': details}) as response:
            response.raise_for_status()
            return response.json()


def put_json(session, url, python_obj):
    """Put json content and decode json response."""
    with session.put(url, json=python_obj) as response:
        response.raise_for_status()
        return response.json()