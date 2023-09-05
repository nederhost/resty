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

    def __init__(self, *arg, url='https://api.mollie.nl/v2', testmode=False, **kwarg):
        """
        Arguments in addition to those of the base class:
        * url -- the URL of the Mollie API
        * testmode -- if true enable testmode for all calls through this
          client (required when testing with organizational access tokens)
        """
        resty.client.Client.__init__(
            self,
            root=url,
            *arg,
            **kwarg
        )
        self.testmode = testmode

    def serialize_hook(self, request):
        if self.testmode:
            if request.parameters is None:
                request.parameters = {}
            if request.method == 'GET':
                request.parameters['testmode'] = 'true'
            else:
                request.parameters['testmode'] = True
