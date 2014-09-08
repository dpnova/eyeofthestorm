import json


class Renderer(object):
    media_type = "application/json"
    charset = None

    def render(self, response_data, context, accepted_media_type):
        """
        Offensively simple renderer

        Please overwrite this method in subclasses for specific render types.
        """
        return json.dumps(response_data)
