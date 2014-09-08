"""
Eventually we'll probably want to add some decent serialization support.

For now - this is a pass through. Patches accepted :)
"""

class Serializer(object):
    def serialize(cls, obj):
        return obj

    def is_valid(self):
        return True
