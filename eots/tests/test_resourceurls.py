"""Tests for the resourceurls helpers"""

from twisted.trial import unittest
from eots.resourceurls import URLList
from eots.resources import ResourceSet


class RS(ResourceSet):
    pass


class ResourceURLsTest(unittest.TestCase):
    def test_urllist(self):
        l = URLList([])
        l.register(RS("testing"))
        l.append("foo")
        urls = l.urls
        self.assertEqual(len(urls), 3)

    def test_suburllist(self):
        l = URLList([])
        p = RS("parent")
        c = RS("child")
        with l.register(p) as parent:
            parent.register(c)
        print l.urls
