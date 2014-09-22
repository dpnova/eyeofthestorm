import json
from eots.utils import encoders
from cyclone.httputil import _parse_header as parse_header
import six


class Renderer(object):
    media_type = "application/json"
    charset = None

    def render(self, response_data, context, accepted_media_type):
        """
        Offensively simple renderer

        Please overwrite this method in subclasses for specific render types.
        """
        return json.dumps(response_data)


class JSONRenderer(Renderer):
    """
    Renderer which serializes to JSON.
    Applies JSON's backslash-u character escaping for non-ascii characters.

    From DRF.
    """

    media_type = 'application/json'
    format = 'json'
    encoder_class = encoders.JSONEncoder
    ensure_ascii = True

    # We don't set a charset because JSON is a binary encoding,
    # that can be encoded as utf-8, utf-16 or utf-32.
    # See: http://www.ietf.org/rfc/rfc4627.txt
    # Also: http://lucumr.pocoo.org/2013/7/19/application-mimetypes-and-encodings/
    charset = None

    def get_indent(self, accepted_media_type, renderer_context):
        if accepted_media_type:
            # If the media type looks like 'application/json; indent=4',
            # then pretty print the result.
            base_media_type, params = parse_header(accepted_media_type.encode('ascii'))
            try:
                return max(min(int(params['indent']), 8), 0)
            except (KeyError, ValueError, TypeError):
                pass

        # If 'indent' is provided in the context, then pretty print the result.
        # E.g. If we're being called by the BrowsableAPIRenderer.
        return renderer_context.get('indent', None)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return bytes()

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        ret = json.dumps(
            data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii
        )

        # On python 2.x json.dumps() returns bytestrings if ensure_ascii=True,
        # but if ensure_ascii=False, the return type is underspecified,
        # and may (or may not) be unicode.
        # On python 3.x json.dumps() returns unicode strings.
        if isinstance(ret, six.text_type):
            return bytes(ret.encode('utf-8'))
        return ret
