from cyclone.web import HTTPError


class RESTException(Exception):
    pass


class UnversionedResourceException(RESTException):
    pass


class NoRendererException(RESTException):
    pass


class ResourceVersionNotFoundError(HTTPError, RESTException):
    pass
