"""
Postcode.NL API client.

# Usage
```
import resty.api.kvknl

client = resty.api.postcodenl.PostcodeNLClient()
client.set_authorization('username', 'password')
root = client.api

organisations = root.zoeken.get(handelsnaam='NederHost'


```
"""

import resty.client
import resty.auth.basicauth

class PostcodeNLClient(resty.client.Client):
    """
    The Postcode.NL API client.
    """

    def __init__(self, *arg, url='https://api.postcode.eu/nl/v1', **kwarg):
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
