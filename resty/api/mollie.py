"""
Mollie API client.

# Usage
```
import resty.api.mollie

client = resty.api.mollie.MollieClient(debuglevel=1)
client.set_authorization('live_MAjw8Ah5hVSkjewtFS')

payments = client.payments.get()
```
"""

import resty.client
import resty.auth

class MollieClient(resty.client.Client):
    """
    The Mollie API client.
    """

    def __init__(self, *arg, url='https://api.mollie.nl/v2', **kwarg):
        """
        Arguments in addition to those of the base class:
        * url -- the URL of the Mollie API
        """
        resty.client.Client.__init__(
            self,
            root=url,
            *arg,
            **kwarg
        )
