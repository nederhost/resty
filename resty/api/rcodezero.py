"""
RcodeZero API client.

# Usage
```
import resty.api.rcodezero

client = resty.api.rcodezero.RcodeZeroClient(url='https://my.rcodezero.at/api/v2')
client.set_authorization('s3cr3tap1k3y')

zone = client.api.server.zones('zonename.com').get()
```
"""

import json

import resty.client
import resty.auth

class RcodeZeroClient(resty.client.Client):
    """
    The RcodeZero API client.
    """

    def __init__(self, *arg, url, **kwarg):
        """
        Arguments in addition to those of the base class:
        * url -- the URL of the RcodeZero API
        """
        resty.client.Client.__init__(
            self,
            root=url,
            auth=resty.auth.headerauth.Authorization(),
            *arg,
            **kwarg
        )
        
    def get_error_content(self, exc):
        """
        Parse the content from a raised exception by trying to interpret the
        content as JSON.
        """
        return json.loads(exc.content)
