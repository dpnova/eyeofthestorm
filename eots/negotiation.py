from __future__ import absolute_import

from .exceptions import NoRendererException, ResourceVersionNotFoundError
from .utils.mediatypes import order_by_precedence, media_type_matches
from .utils.mediatypes import _MediaType
from cyclone.httputil import _parse_header as parse_header


class ContentNegotiator(object):
    def select_renderer(self, request, renderers):
        """
        Use the accept header to decide which renderer to use.
        """
        accept_header_val = request.headers['Accept']
        accepts = accept_header_val.split(",")
        for media_type_set in order_by_precedence(accepts):
            for renderer in renderers:
                for media_type in media_type_set:
                    if media_type_matches(renderer.media_type, media_type):
                        # Return the most specific media type as accepted.
                        if (
                            _MediaType(renderer.media_type).precedence >
                            _MediaType(media_type).precedence
                        ):
                            # Eg client requests '*/*'
                            # Accepted media type is 'application/json'
                            return renderer, renderer.media_type
                        else:
                            # Eg client requests 'application/json; indent=8'
                            # Accepted media type 'application/json; indent=8'
                            return renderer, media_type
        raise NoRendererException("No valid renderer found for this version.")

    def select_parser(self, request, parsers):
        """
        Given the request return a parser for the content type.
        """
        for parser in parsers:
            if media_type_matches(
                    parser.media_type,
                    request.headers.get("Content-Type", "")):
                return parser
        return None


class VersionNegotiator(object):
    def get_version(self, request):
        return None


class AcceptsVersionNegotiator(VersionNegotiator):
    """
    Default version negotiator.

    This uses the Accept header but can fallback to the "v" query param.
    """
    def get_version(self, request):
        version = None

        # Attempt to get version from Accept header
        accepts = request.headers.get("Accept")
        if accepts:
            _, params = parse_header(accepts)
            version = params.get('v')

        # Attempt to get version from query params
        if not version:
            try:
                version = request.arguments['v'][0]
            except (KeyError, TypeError, IndexError):
                pass

        return version

    def select_version(self, request, versions):
        """
        Return the resource for the current version.

        Potentially we could try and order versions and choose the most
        up to date one in the situation where a client has simply
        forgotten to add the version.
        """
        version = self.get_version(request)
        try:
            return versions[version]
        except (KeyError, ValueError):
            try:
                return versions[int(version)]
            except (ValueError, KeyError):
                try:
                    return versions[float(version)]
                except:
                    pass
        raise ResourceVersionNotFoundError(404)
