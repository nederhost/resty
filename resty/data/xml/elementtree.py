import resty.data

import xml.etree.ElementTree

class Serializer(resty.data.SerializerBase):

    # Set the content type as class variable for easier modification by
    # specific client implementations.
    contenttype = 'application/xml'

    def serialize(self, request):
        request.set_data(request.dump(), self.contenttype)
        
class Parser(resty.data.ParserBase):
    def parse(self, response):
        response.content = xml.etree.ElementTree.fromstring(response.raw_response)
