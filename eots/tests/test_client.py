from mock import patch

from twisted.trial import unittest
from eots.client import RESTClient


class RESTClientTest(unittest.TestCase):
    @patch('eots.client.treq')
    def test_auth_is_used_when_passed(self, treq_mock):
        username, password = 'user', 'hunter2'
        client = RESTClient('http://base/', auth=(username, password))
        client.retrieve('resource', 1)
        args, kwargs = treq_mock.request.call_args
        self.assertTrue(kwargs['auth'] == (username, password))
