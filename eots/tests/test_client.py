#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Test the eots client module."""
from mock import patch, Mock

from twisted.trial import unittest
from eots.client import RESTClient, EOTSResponse


class RESTClientTest(unittest.TestCase):
    """Test basic authentication in eots."""

    @patch('eots.client.treq')
    def test_auth_is_used_when_passed(self, treq_mock):
        """Test succesful user authentication."""
        username, password = 'user', 'hunter2'
        client = RESTClient('http://base/', auth=(username, password))
        client.retrieve('resource', 1)
        args, kwargs = treq_mock.request.call_args
        self.assertTrue(kwargs['auth'] == (username, password))

    @patch('eots.client.treq')
    def test_utf8(self, treq_mock):
        """Test succesful user authentication."""
        username, password = 'user', 'hunter2'
        client = RESTClient(
            'http://base/',
            auth=(username, password),
        )
        client.list(
            'resource',
            params={'search': u"pijamalı hasta yağız şoföre çabucak güvendi"}
        )
        args, kwargs = treq_mock.request.call_args
        self.assertTrue(kwargs['auth'] == (username, password))


class EOTSResponseTest(unittest.TestCase):
    """Test the eots reponse for a request."""

    def test_get_complete_content(self):
        """Test succesful content acquisition."""
        response = Mock()
        response.content = "none"
        er = EOTSResponse(response)
        self.assertIsNone(er.complete_content)
        self.assertIsNone(er.complete_json)
        r = er.content
        self.assertEqual(r, "none")
