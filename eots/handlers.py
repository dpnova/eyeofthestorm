from cyclone.web import RequestHandler
from twisted.internet.defer import maybeDeferred, inlineCallbacks
from twisted.python import log
import json


class RESTHandler(RequestHandler):
    parsed_body = None

    def initialize(self, **kwargs):
        """
        Resource set is a structure holding resources of various versions.

            resource_set = {
                "v1": V1ProfileResource
            }

        Each request will check the Accept header to find the resource version
        and serialization format:

            Accept: application/vnd.servicename+json; version=v1

        The locale is also passed to the Resource in case it needs to
        provide specific language data. Note: Use the Accept-Language header.
        """
        self.resource_set = kwargs.pop("resource_set")
        self.is_detail = kwargs.pop("is_detail", False)
        super(RESTHandler, self).initialize(**kwargs)
        self.resource = \
            self.resource_set.resource_for_request(self, **kwargs)
        self.resource.set_locale(self.locale)

    def get_current_user(self):
        return self.resource.perform_authentication()

    def prepare(self):
        """
        Run the pre-handling tasks.

        Notably we want to make sure we're not breaking some policy
        by processing this request (auth/permissions/rate limits etc)
        """
        self.resource.check_permissions()
        self.resource.check_throttles()
        self.resource.perform_content_negotiation()
        self.parsed_body = self.resource.accepted_parser.parse(
            self.request.body)

    def get_template_namespace(self):
        """
        The cyclone namespace method to provide our required context.

        By overriding this we skip unnecessary work by the cyclone handler.
        """
        return self.resource.renderer_context()

    @inlineCallbacks
    def render(self, response_data, **kwargs):
        """
        Once we have get a response, we need to render it and return.

        We use the serializer to get a dict version of the data returned.
        We use the renderer to turn it into whatever content was requested
        as part of the content negotiation process.

        Finally we can set the character encoding and the relevant content type
        before finishing the request from the client.
        """
        response_data = yield self.resource.apply_serializer(response_data)
        context = self.get_template_namespace()
        context.update(kwargs)
        data, media_type, charset = yield self.resource.apply_renderer(
            response_data, context)

        content_type = media_type
        if charset:
            content_type = "%s; charset=%s" % (media_type, charset)

        self.set_header("Content-Type", content_type)
        self.finish(data)

    def get(self, id=None):
        """
        Handle HTTP GET requests.

        If the url had an ID we fetch a specific resource, otherwise we
        fetch a list of items.
        """
        if not id:
            return maybeDeferred(self.resource.list).addCallback(self.render)
        return maybeDeferred(
            self.resource.retrieve, id).addCallback(self.render)

    def head(self, id=None):
        return self.get(id)

    def post(self, id=None):
        """Accept a POST request to create a new object"""

        def before_render(result):
            """Set headers etc before rendering content"""
            self.set_header(
                "Location",
                self.request.path + "/" +
                str(self.resource.get_id_for_response(result))
            )
            self.set_status(201)
            return result

        return maybeDeferred(
            self.resource.create, self.parsed_body
        ).addCallback(
            before_render,
        ).addCallback(
            self.render
        )

    def delete(self, id=None):
        pass

    def patch(self, id=None):
        pass

    def put(self, id=None):
        """Accept a PUT request to update an existing object"""
        return maybeDeferred(
            self.resource.update, self.parsed_body
        ).addCallback(
            self.render
        )

    def options(self, id=None):
        pass

