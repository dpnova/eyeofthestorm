"""
A simple client for interacting with a REST interface.

FIXME: Note hard coded json as request body! We need to fix this.
"""
from twisted.internet.defer import inlineCallbacks
from twisted.python import log
import treq
import json


class EOTSResponse(object):
    def __init__(self, treq_request):
        self._t_request = treq_request
        self.complete_content = None

    def __getattr__(self, name):
        return getattr(self._t_request, name)


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
        return self._make_request(
            "GET",
            self._full_url(path, id),
            **kwargs
        )

    def list(self, path, *args, **kwargs):
        return treq.get(
            self._full_url(path))

    def update(self, path, id, **kwargs):
        return self._make_request(
            "PUT",
            self._full_url(path, id),
            **kwargs
        )

    def delete(self, path, id, *args, **kwargs):
        return treq.delete(
            self._full_url(path, id),
            headers=self._all_extra_headers())

    def create(self, path, data, **kwargs):
        path = self._full_url(path)
        return self._make_request("POST", path, data=data, **kwargs)

    def info(self, path, id=None, *args, **kwargs):
        return treq.options(
            self._full_url(path, id),
            headers=self._all_extra_headers())

    def _make_request(self, method, path, data=None, *args, **kwargs):
        data = json.dumps(data) if data is not None else None
        headers = self._all_extra_headers()
        new_headers = kwargs.pop("headers", {})
        headers.update(new_headers)
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
        eots_response = EOTSResponse(response)
        return response.content().addCallback(self.got_content, eots_response)

    def got_content(self, content, response):
        response.complete_content = content
        response.complete_json = json.loads(content)
        return response

