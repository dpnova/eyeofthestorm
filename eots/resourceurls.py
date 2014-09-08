from cyclone.web import url


def add_versioned_resource_urls(urls, resource_set, prefix="", data=None):
    urls.extend(resource_set.get_urls(prefix=prefix, data=data))
    return urls
