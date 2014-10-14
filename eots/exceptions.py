from cyclone.web import HTTPError


class RESTException(Exception):
    pass


class UnversionedResourceException(RESTException):
    pass


class NoRendererException(RESTException):
    pass


class ResourceVersionNotFoundError(HTTPError, RESTException):
    pass


class UnsupportedMediaType(HTTPError, RESTException):
    pass


class ParseError(RESTException):
    pass


class AuthFailedError(HTTPError, RESTException):
    pass
