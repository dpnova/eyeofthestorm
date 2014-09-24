from mock import Mock
from twisted.trial import unittest

from eots.exceptions import NoRendererException
from eots.negotiation import ContentNegotiator, AcceptsVersionNegotiator


class ContentNegotiatorTest(unittest.TestCase):
    def setUp(self):
        self.request = Mock()
        self.request.headers = {"Accept": "text/html"}
        self.negotiator = ContentNegotiator()

        self.renderers = [
            Mock(media_type="text/html", name="html"),
            Mock(media_type="application/json", name="json"),
        ]

    def test_select_renderer_basic(self):
        r = self.negotiator.select_renderer(self.request, self.renderers)
        self.assertEqual(r[0], self.renderers[0])

    def test_select_renderer_more(self):
        self.request.headers = {"Accept": "application/json"}
        r = self.negotiator.select_renderer(self.request, self.renderers)
        self.assertEqual(r[0], self.renderers[1])

    def test_select_renderer_wildcard(self):
        self.request.headers = {"Accept": "application/*"}
        r = self.negotiator.select_renderer(self.request, self.renderers)
        self.assertEqual(r[0], self.renderers[1])

    def test_select_renderer_fail(self):
        self.request.headers = {"Accept": "application/xml"}
        self.assertRaises(
            NoRendererException,
            self.negotiator.select_renderer,
            self.request,
            self.renderers
        )


class AcceptsVersionNegotiatorTest(unittest.TestCase):
    def test_get_version(self):
        request = Mock()
        request.headers = {"Accept": "text/html; v=1"}
        self.assertEqual("1", AcceptsVersionNegotiator().get_version(request))

    def test_get_version_returns_None_when_no_version_specified(self):
        request = Mock()
        request.headers = {"Accept": "text/html"}
        self.assertEqual(None, AcceptsVersionNegotiator().get_version(request))

    def test_get_version_will_fallback_to_query_params(self):
        request = Mock()
        request.headers = {"Accept": "text/html"}
        request.arguments = {'v': [1]}
        self.assertEqual(1, AcceptsVersionNegotiator().get_version(request))
