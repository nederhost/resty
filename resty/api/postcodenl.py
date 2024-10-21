"""
Postcode.NL API client.

# Usage
```
import resty.api.postcodenl

client = resty.api.postcodenl.PostcodeNLClient()
client.set_authorization('username', 'password')
root = client.api
address = root.addresses.route('1234AB').route('123').get()
```
"""

import resty.client
import resty.auth.basicauth
import urllib.parse

class PostcodeNLClient(resty.client.Client):
    """
    The Postcode.NL API client.
    """

    def __init__(self, *arg, url='https://api.postcode.eu', **kwarg):
        """
        Arguments in addition to those of the base class:
        * url -- the URL of the Postcode.NL API
        """
        resty.client.Client.__init__(
            self,
            root=url,
            auth=resty.auth.basicauth.Authorization(),
            *arg,
            **kwarg
        )
        self.__autocomplete_session = None
        self.transport.parameter_quoter = urllib.parse.quote	# encode spaces as %20
        
    def set_autocomplete_session(self, value=None):
        """
        Set the specified value as the X-Autocomplete-Session header on
        subsequent requests.  Set the value to None to disable sending the
        header.
        """
        self.__autocomplete_session = value
        
    def request_hook(self, request):
        # Add the autocomplete session header if required.
        if self.__autocomplete_session is not None:
            request.headers['X-Autocomplete-Session'] = self.__autocomplete_session
            