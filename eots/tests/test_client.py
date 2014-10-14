from mock import patch, Mock

from twisted.trial import unittest
from eots.client import RESTClient, EOTSResponse


class RESTClientTest(unittest.TestCase):
    @patch('eots.client.treq')
    def test_auth_is_used_when_passed(self, treq_mock):
        username, password = 'user', 'hunter2'
        client = RESTClient('http://base/', auth=(username, password))
        client.retrieve('resource', 1)
        args, kwargs = treq_mock.request.call_args
        self.assertTrue(kwargs['auth'] == (username, password))


class EOTSResponseTest(unittest.TestCase):
    def test_get_complete_content(self):
        response = Mock()
        response.content = "none"
        er = EOTSResponse(response)
        self.assertIsNone(er.complete_content)
        self.assertIsNone(er.complete_json)
        r = er.content
        self.assertEqual(r, "none")
