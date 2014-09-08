from cyclone.web import Application

from eots import RESTResource, ResourceSet, add_versioned_resource_urls


class TestResource(RESTResource):
    def list(self):
        return ["meow"]


class V2TestResource(TestResource):
    pass


class AnotherResource(RESTResource):
    pass


class SomeOtherResource(RESTResource):
    pass

class MyOwnResourceSet(ResourceSet):
    slug = "someother"
    versions = {"v1": SomeOtherResource}


class TestRestApplication(Application):
    def __init__(self):
        handlers = []
        add_versioned_resource_urls(
            handlers,
            ResourceSet("test", {1: TestResource, 2: V2TestResource}),
            prefix="/api")
        add_versioned_resource_urls(
            handlers,
            ResourceSet("another", {1: AnotherResource, 2: AnotherResource}),
            prefix="/api")
        add_versioned_resource_urls(
            handlers,
            MyOwnResourceSet(),
            prefix="/api")
        Application.__init__(self, handlers, debug=True)
