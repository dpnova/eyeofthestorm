from cyclone.httpserver import HTTPRequest
from cyclone.web import Application
from mock import Mock
from twisted.trial import unittest
from twisted.internet.defer import succeed
from twisted.python import log

from eots import ResourceSet
from eots.handlers import RESTHandler


class RESTHandlerTest(unittest.TestCase):
    def setUp(self):
        self.app = Application()
        self.request = HTTPRequest("GET", "/", connection=Mock())
        self.request.headers["Accept"] = "application/json; v=v1"
        self.resource_class = Mock()
        self.handler = RESTHandler(
            self.app, self.request,
            resource_set=ResourceSet("test", versions={"v1": self.resource_class}))
        self.handler._transforms = []
        self.handler._request_summary = lambda: None
        self.app.log_request = lambda x: None

    def test_initialize(self):
        self.assertTrue(hasattr(self.handler, "resource_set"))

    def test_get(self):
        self.resource_class.return_value.list.return_value = "['item']"
        self.resource_class.return_value.apply_renderer.return_value = \
            "['item']", "app/json", "utf8"

        def handle_result(result):
            self.assertEqual(result, None)
            res = self.request.connection.write.call_args_list[0][0][0]
            self.assertTrue("['item']" in res)

        return self.handler.get().addBoth(handle_result)

    def test_get_id(self):
        self.resource_class.return_value.retrieve.return_value = "something"
        self.resource_class.return_value.apply_renderer.return_value = \
            "something", "app/json", "utf8"

        def handle_result(result):
            self.assertEqual(result, None)
            res = self.request.connection.write.call_args_list[0][0][0]
            self.assertTrue("something" in res)
            # self.assertEqual(self.handler._write_buffer, ["something"])

        return self.handler.get(id=1).addBoth(handle_result)

    def test_prepare(self):
        self.handler.resource = Mock()
        self.handler.prepare()
        self.handler.resource.check_permissions.assert_called_with()
        self.handler.resource.check_throttles.assert_called_with()
        self.handler.resource.perform_content_negotiation.assert_called_with()

    def test_head(self):
        self.resource_class.return_value.list.return_value = "['item']"
        self.resource_class.return_value.apply_renderer.return_value = \
            "['item']", "app/json", "utf8"

        def handle_result(result):
            self.assertEqual(result, None)
            res = self.request.connection.write.call_args_list[0][0][0]
            self.assertTrue("['item']" in res)
        return self.handler.head().addBoth(handle_result)

    def test_post(self):
        self.handler.resource.create.return_value = "['item']"
        self.handler.render = Mock(return_value=succeed(None))

        def cb(result):
            self.assertEqual(result, None)
            self.handler.render.assert_called_with("['item']")
        return self.handler.post().addCallbacks(cb, log.err)

    def test_delete(self):
        self.handler.resource.delete.return_value = None
        self.handler.render = Mock(return_value=succeed(None))

        def handle_result(result):
            self.handler.render.assert_called_with(None)
            self.assertTrue(self.handler._status_code, 204)

        return self.handler.delete().addBoth(handle_result)

    def test_patch(self):
        self.handler.patch()

    def test_put(self):
        self.handler.render = Mock()
        self.handler.return_value = None
        self.handler.put()

    def test_options(self):
        self.handler.options()

