from twisted.trial import unittest
from mock import Mock
from eots.permissions import Permission, OwnerCanModify


class PermissionTest(unittest.TestCase):
    def setUp(self):
        self.resource = Mock()
        self.handler = Mock()
        self.perm = Permission()

    def test_can_read(self):
        self.assertTrue(self.perm.can_read(self.handler, self.resource))

    def test_can_write(self):
        self.assertTrue(self.perm.can_write(self.handler, self.resource))


class OwnerCanModifyTest(unittest.TestCase):
    def setUp(self):
        self.resource = Mock()
        self.handler = Mock()
        self.perm = OwnerCanModify()

    def test_can_write_anon(self):
        self.resource.get_owner.return_value = None
        self.handler.get_current_user.return_value = None
        self.assertFalse(self.perm.can_write(self.handler, self.resource))
