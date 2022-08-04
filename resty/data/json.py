"""
JSON serializer and parser.
"""

import json

import resty.data

class Serializer(resty.data.SerializerBase):
    """
    JSON serializer.
    """

    # Set the content type as class variable for easier modification by
    # specific client implementations.
    contenttype = 'application/json'

    def serialize(self, request):
        """
        Serialize the request to JSON.

        See json.dumps() for more information on serializing Python objects.
        """
        if request.parameters is not None:
            request.set_data(json.dumps(request.parameters), self.contenttype)

class Parser(resty.data.ParserBase):
    """
    JSON parser.
    """

    def parse(self, response): # pylint: disable=no-self-use
        """
        Parse the JSON response to Python objects.

        See json.loads() for more information.
        """
        response.content = json.loads(response.raw_response)
