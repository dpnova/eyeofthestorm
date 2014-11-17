
class SubURLList(object):
    def __init__(self, handlers, parent_resourceset, prefix, data):
        self._handlers = handlers
        self._parent_resourceset = parent_resourceset
        self._prefix = prefix
        self._data = data

    def register(self, resourceset, data=None):
        urls = resourceset.get_nested_urls(
            self._parent_resourceset,
            self._prefix,
            self._data
        )
        self._handlers.extend(urls)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


class URLList(object):
    def __init__(self, handlers=None):
        self._handlers = handlers or []

    def register(self, resourceset, prefix="", data=None):
        urls = resourceset.get_urls(prefix, data)
        self._handlers.extend(urls)
        return SubURLList(self._handlers, resourceset, prefix, data)

    def append(self, url):
        """Providing some list-ish interface."""
        self._handlers.append(url)

    @property
    def urls(self):
        return self._handlers
