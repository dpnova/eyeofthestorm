import json


class Parser(object):
    def parse(self, data):
        return


class JSONParser(Parser):
    media_type = "application/json"

    def parse(self, data):
        return json.loads(data)
