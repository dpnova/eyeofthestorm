from twisted.trial import unittest
from mock import Mock
from eots.permissions import Permission, IsOwnerOrReadOnly


class PermissionTest(unittest.TestCase):
    def setUp(self):
        self.resource = Mock()
        self.handler = Mock()
        self.perm = Permission()

    def test_has_permission(self):
        self.assertTrue(self.perm.has_permission(self.handler, self.resource))


class IsOwnerOrReadOnlyTest(unittest.TestCase):
    def setUp(self):
        self.resource = Mock()
        self.handler = Mock()
        self.perm = IsOwnerOrReadOnly()

    def test_can_write_anon(self):
        obj = Mock()
        obj.get_owner.return_value = None
        obj.get_current_user.return_value = None
        self.assertFalse(
            self.perm.has_object_permission(self.handler, self.resource, obj))
