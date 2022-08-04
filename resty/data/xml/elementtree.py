"""
XML serialiation and parsing support using ElementTree.
"""

import xml.etree.ElementTree

import resty.data

class Serializer(resty.data.SerializerBase):
    """
    XML serializer that accepts xml.etree.ElementTree objects.
    """

    # Set the content type as class variable for easier modification by
    # specific client implementations.
    contenttype = 'application/xml'

    def serialize(self, request):
        """
        Serialize the request.

        The request must be an instance of xml.etree.ElementTree or
        compatible class.
        """
        request.set_data(request.dump(), self.contenttype)

class Parser(resty.data.ParserBase):
    """
    XML parser that produces xml.etree.ElementTree objects.
    """

    def parse(self, response): # pylint: disable=no-self-use
        """
        Parse the XML response.

        Return an instance of xml.etree.ElementTree.
        """
        response.content = xml.etree.ElementTree.fromstring(response.raw_response)
