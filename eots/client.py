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
    def __init__(self, base_url=None, version=None, auth=None):
        self.base_url = self.base_url or base_url or ""
        self.version = self.version or version or 0
        self.accept_content_type = "application/json"
        self.auth = auth

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
        return self._make_request(
            "GET",
            self._full_url(path, id),
            **kwargs
        )

    def list(self, path, *args, **kwargs):
        return self._make_request(
            "GET",
            self._full_url(path),
            **kwargs
        )

    def update(self, path, id, **kwargs):
        return self._make_request(
            "PUT",
            self._full_url(path, id),
            **kwargs
        )

    def delete(self, path, id, *args, **kwargs):
        return self._make_request(
            "DELETE",
            self._full_url(path, id),
            **kwargs
        )

    def create(self, path, data, **kwargs):
        path = self._full_url(path)
        return self._make_request("POST", path, data=data, **kwargs)

    def info(self, path, id=None, *args, **kwargs):
        return self._make_request(
            "OPTIONS",
            self._full_url(path, id),
            **kwargs
        )

    def _make_request(self, method, path, data=None, *args, **kwargs):
        data = json.dumps(data) if data is not None else None
        headers = self._all_extra_headers()
        new_headers = kwargs.pop("headers", {})
        headers.update(new_headers)

        if self.auth:
            kwargs['auth'] = self.auth

        return treq.request(
            method,
            path,
            headers=headers,
            data=data,
            **kwargs
        ).addCallbacks(
            self._handle_response,
            log.err
        )

    def _handle_response(self, response):
        return response.json().addCallback(
            lambda content: (response, content))
