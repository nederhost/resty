import resty.data

import json

class Serializer(resty.data.SerializerBase):

    # Set the content type as class variable for easier modification by
    # specific client implementations.
    contenttype = 'application/json'

    def serialize(self, request):
        if request.parameters is not None:
            request.set_data(json.dumps(request.parameters), self.contenttype)
        
class Parser(resty.data.ParserBase):
    def parse(self, response):
        response.content = json.loads(response.raw_response)
