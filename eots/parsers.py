import json
from .exceptions import ParseError
import six


class Parser(object):
    def parse(self, data):
        return


class JSONParser(Parser):
    """
    Parses JSON-serialized data.
    """

    media_type = 'application/json'

    def parse(self, data, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as JSON and returns the resulting data.
        """
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', "utf-8")
        if not data:
            return
        try:
            data = data.decode(encoding)
            return json.loads(data)
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % six.text_type(exc))
