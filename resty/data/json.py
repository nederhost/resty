"""
JSON serializer and parser.
"""

import decimal
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
            request.set_data(json.dumps(request.parameters, default=serializer), self.contenttype)

class Parser(resty.data.ParserBase):
    """
    JSON parser.
    """

    def parse(self, response): # pylint: disable=no-self-use
        """ 
        
        Parse the JSON of any response that either has no content-type
        header or a content-type header with MIME type 'application/json' to
        Python objects.

        See json.loads() for more information.
        """
        if (
          'content-type' not in response.headers or
          response.headers['content-type'].endswith('/json') or
          response.headers['content-type'].endswith('+json')
        )
            response.content = json.loads(response.raw_response)

def serializer(object):
    """
    Support for some additional data types.
    """
    if isinstance(object, decimal.Decimal):
        return float(object)
    raise TypeError(f'Object {object} is not serializable')
