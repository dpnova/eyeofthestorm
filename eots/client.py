"""
A simple client for interacting with a REST interface.

FIXME: Note hard coded json as request body! We need to fix this.
"""
from twisted.python import log
from cyclone.escape import utf8
import treq
import json


class EOTSResponse(object):
    def __init__(self, treq_request):
        self._t_request = treq_request
        self.complete_content = None
        self.complete_json = None

    def body(self, raw=False):
        if raw:
            return self.complete_content
        return self.complete_json

    def __getattr__(self, name):
        return getattr(self._t_request, name)


class RESTClient(object):
    base_url = None
    version = None

    def __init__(self, base_url=None, version=None, auth=None):
        """"""
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
        """Parse and create the request object."""
        data = json.dumps(data) if data is not None else None
        headers = self._all_extra_headers()
        new_headers = kwargs.pop("headers", {})
        headers.update(new_headers)

        if self.auth:
            kwargs['auth'] = self.auth

        if kwargs.get('params', {}):
            params = kwargs.get('params', {})

            for key, value in params.items():
                value = utf8(value) if isinstance(value, basestring) else value
                params[key] = value
            if params:
                kwargs['params'] = params

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
