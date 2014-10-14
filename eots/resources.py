from cyclone.web import url
from twisted.internet.defer import maybeDeferred, inlineCallbacks, returnValue

from .authentication import Authenticator
from .handlers import RESTHandler
from .negotiation import ContentNegotiator, AcceptsVersionNegotiator
from .permissions import Permission
from .renderers import Renderer, JSONRenderer
from .serializers import Serializer
from .parsers import JSONParser
from .exceptions import (
    UnversionedResourceException, ResourceVersionNotFoundError,
    UnsupportedMediaType)


def _url_with_prefix(prefix, url):
    return "/".join([prefix, url])


class ResourceSet(object):
    """
    A set of RESTResource versions.
    """
    label = None
    slug = None
    versions = None
    handler = RESTHandler
    version_negotiator_class = AcceptsVersionNegotiator
    _unversioned = False

    def __init__(self, slug=None, versions=None, handler=None):
        self.versions = self.versions or versions or {}
        self.slug = slug or self.slug
        self.handler = handler or self.handler

    @classmethod
    def unversioned(cls, slug, resource=None, handler=None):
        """
        Create an unversioned resource set.
        """
        self = cls(slug, handler, versions={None: resource})
        self._unversioned = True
        return self

    def add_versions(self, versions):
        """
        Add new versions to this resource.

        We don't use kwargs here because versions will frequently be numbers.
        Note: This will replace existing resources with the same version.
        """
        if self.unversioned:
            raise UnversionedResourceException(
                "Can not add more versions to an unversioned resource")
        self.versions.update(versions)

    def get_version_from_request(self, request):
        version = self.version_negotiator_class().select_version(
            request, self.versions)
        return version

    def resource_for_request(self, handler, **kwargs):
        resource_class = self.get_version_from_request(handler.request)
        resource = resource_class()
        resource.initialize(handler, **kwargs)
        return resource

    def get_urls(self, prefix="", data=None):
        """
        Get the set of urls for this rest resource.

        /prefix/slug
        /prefix/slug/(\d+)
        """
        slug = self.__class__.__name__.lower() if not self.slug else self.slug
        detail_handler_data = {
            "resource_set": self,
            "is_detail": True
        }
        list_handler_data = {
            "resource_set": self
        }
        detail_handler_data.update(data or {})
        list_handler_data.update(data or {})
        return [
            url(
                _url_with_prefix(prefix, slug) + r"/(.+)$",
                self.handler, name="%s_root" % self.slug,
                kwargs=detail_handler_data),
            url(
                _url_with_prefix(prefix, slug),
                self.handler, name="%s_detail" % self.slug,
                kwargs=list_handler_data),
        ]


class RESTResource(object):
    """
    A version of a resource.

    Since available serializers, renderers etc may change between versions
    they are defined in subclasses of this.

    Also permissions are checked here as they may vary depending on the
    operation being performed (read/write/etc).

    Finally, though it may seem odd, we also do auth here. This allows
    the flexibility to include/deprecate certain auth methods between
    versions.
    """
    serializer_class = Serializer
    renderer_classes = [JSONRenderer]
    permission_classes = [Permission]
    authentication_classes = [Authenticator]
    parser_classes = [JSONParser]
    content_negotiation_class = ContentNegotiator

    locale = None
    version = None
    accepted_renderer = None
    media_type = None
    handler = None

    _authenticator = None
    _user = None
    _auth = None

    def initialize(self, handler, **kwargs):
        self.handler = handler
        self.kwargs = kwargs

    def retrieve(self, id):
        raise NotImplementedError(
            "You must implement retrieve() on your Resource")

    def list(self):
        raise NotImplementedError(
            "You must implement list() on your Resource")

    def create(self, **kwargs):
        raise NotImplementedError(
            "You must implement create() on your Resource")

    def delete(self, id):
        raise NotImplementedError(
            "You must implement delete() on your Resource")

    def update(self, id, **kwargs):
        raise NotImplementedError(
            "You must implement update() on your Resource")

    def info(self):
        raise NotImplementedError(
            "You must implement options() on your Resource")

    def status(self, id=None):
        raise NotImplementedError(
            "You must implement status() on your Resource")

    def set_locale(self, locale):
        self.locale = locale

    def perform_authentication(self):
        for authenticator in self.get_authenticators():
            auth_results = authenticator.authenticate(self.handler)
            if auth_results is not None:
                self._authenticator = authenticator
                self._user, self._auth = auth_results
                return self._user
        self._not_authenticated()

    def _not_authenticated(self):
        self._authenticator = None
        self._user = None
        self._auth = None

    def check_permissions(self):
        for permission in self.get_permissions():
            permission.has_permission(self.handler, self)

    def check_throttles(self):
        pass

    def apply_serializer(self, data):
        return maybeDeferred(self.get_serializer().serialize, data)

    def perform_content_negotiation(self):
        negotiator = self.get_content_negotiator()
        renderers = self.get_renderers()
        self.accepted_renderer, self.media_type = \
            negotiator.select_renderer(self.handler.request, renderers)
        self.accepted_parser = negotiator.select_parser(
            self.handler.request, self.get_parsers())

        if not self.accepted_parser:
            raise UnsupportedMediaType

    @inlineCallbacks
    def apply_renderer(self, response_data, context):
        response = yield maybeDeferred(
            self.accepted_renderer.render,
            response_data, self.media_type, context)
        returnValue(
            (response, self.media_type, self.accepted_renderer.charset)
        )

    def renderer_context(self):
        """
        And extra context to send to the renderer.
        """
        return {}

    def get_permissions(self):
        """
        Init the permissions for this resource version.
        """
        return [permission() for permission in self.permission_classes]

    def get_serializer(self):
        """
        Get the serializer for this resource.
        """
        return self.serializer_class()

    def get_renderers(self):
        """
        Get the set of possible renderers for this resource.
        """
        return [renderer() for renderer in self.renderer_classes]

    def get_authenticators(self):
        """
        Get the set of possible authentication methods for this resource.
        """
        return [auth() for auth in self.authentication_classes]

    def get_content_negotiator(self):
        """
        Get the content negotiator for this resource.
        """
        return self.content_negotiation_class()

    def get_parsers(self):
        return [parser() for parser in self.parser_classes]

    def get_id_for_response(self, response):
        """
        Overwrite to allow the handler to get the new object id.

                def get_id_for_response(self, response):
                    return response['data']['id']
        """
        pass
