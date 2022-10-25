"""
KvK.NL API client.

# Usage
```
import resty.api.kvknl

client = resty.api.kvknl.KvKNLClient()
client.set_authorization('my_api_key')
organisations = client.api.zoeken.get(handelsnaam='Foobar BV')
print(organisations.content)
```
"""

import resty.client
import resty.auth

import resty.auth.headerauth

class KvKClient(resty.client.Client):
    """
    The kvk.nl API client.
    """

    def __init__(self, *arg, url='https://api.kvk.nl/api/v1', **kwarg):
        """
        Arguments in addition to those of the base class:
        * url -- the URL of the KvK API
        """
        resty.client.Client.__init__(
            self,
            root=url,
            auth=resty.auth.headerauth.Authorization(headername='apikey', type=None),
            transport=resty.transport.url.Transport(default_charset='utf-8'),
            *arg,
            **kwarg
        )
