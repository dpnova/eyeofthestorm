"""
A simple client for interacting with a REST interface.

FIXME: Note hard coded json as request body! We need to fix this.
"""
from twisted.internet.defer import inlineCallbacks
from twisted.python import log
import treq
import json


class RESTClient(object):
    base_url = None
    version = None
    def __init__(self, base_url=None, version=None):
        self.base_url = self.base_url or base_url or ""
        self.version = self.version or version or 0
        self.accept_content_type = "application/json"

    def _full_url(self, path, id=None):
        url = self.base_url + path
        if id:
            url += "/%s" % id
        return url


    def _all_extra_headers(self):
        return {
            "Accept": "%s; v=%s" % (self.accept_content_type, self.version),
            "Content-Type": self.accept_content_type
        }

    def retrieve(self, path, id, *args, **kwargs):
        return treq.get(
            self._full_url(path, id),
            headers=self._all_extra_headers())

    def list(self, path, *args, **kwargs):
        return treq.get(
            self._full_url(path),
            headers=self._all_extra_headers())

    def update(self, path, id, *args, **kwargs):
        return treq.put(
            self._full_url(path, id),
            headers=self._all_extra_headers())

    def delete(self, path, id, *args, **kwargs):
        return treq.delete(
            self._full_url(path, id),
            headers=self._all_extra_headers())

    def create(self, path, data, **kwargs):
        print data
        return self._make_request("POST", path, data=data, **kwargs)

    def info(self, path, id=None, *args, **kwargs):
        return treq.options(
            self._full_url(path, id),
            headers=self._all_extra_headers())

    def _make_request(self, method, path, data=None, *args, **kwargs):
        data = json.dumps(data) if data is not None else None
        return treq.request(
            method,
            self._full_url(path),
            headers=self._all_extra_headers(),
            data=data,
            **kwargs
        ).addCallbacks(
            self._handle_response,
            log.err
        )

    def _handle_response(self, response):
        return response.json().addCallback(
            lambda content: (response, content))


