from mock import Mock
from twisted.trial import unittest

from eots.resources import RESTResource, _url_with_prefix, ResourceSet


class RESTResourceTest(unittest.TestCase):
    def test_get_urls(self):

        class MyRR(RESTResource):
            slug = "something"
            handler = Mock()

        rs = ResourceSet("myrr", handler=Mock(), versions={"v1": MyRR})
        urls = rs.get_urls()
        self.assertTrue(urls)
        for u in urls:
            self.assertTrue(u.name)
            self.assertEqual(u.handler_class, rs.handler)

    def test_url_with_prefix(self):
        self.assertEqual(
            _url_with_prefix("api", "test"),
            "api/test")
