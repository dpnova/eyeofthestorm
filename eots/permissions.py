
SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
UNSAFE_METHODS = ["PUT", "POST", "DELETE", "PATCH"]

class Permission(object):
    def has_permission(self, handler, resource):
        return True

    def has_object_permission(self, handler, resource, obj):
        return True


class IsOwnerOrReadOnly(Permission):
    def is_owner(self, handler, resource, obj):
        current_user = handler.current_user
        resource_owner = obj.get_owner()
        if (current_user and resource_owner) and current_user == resource_owner:
            return True
        return False

    def has_object_permission(self, handler, resource, obj):
        return self.is_owner(handler, resource)


class IsAdminOrCanCreate(Permission):
    """
    Ensure user is an admin to view data.

    Otherwise just let them create rows.
    """
    def has_permission(self, handler, resource):
        if handler.current_user and handler.current_user.is_admin():
            return True
        elif handler.request.method == "PUT" \
                and not handler.is_detail:
            return True
        return False
