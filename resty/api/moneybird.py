"""
Moneybird API client.

# Usage
```
import resty.api.moneybird

client = resty.api.moneybird.MoneybirdClient()
client.set_authorization('s3cr3tap1k3y')

sales_invoice = client.api.sales_invoice.find_by_invoice_id('12345').get()
```
"""

import resty.client
import resty.auth

class MoneybirdClient(resty.client.Client):
    """
    The Moneybird API client.
    """

    def __init__(self, *arg, admin, url=None, **kwarg):
        """
        Arguments in addition to those of the base class:
        * url -- the URL of the Moneybird API without the administration ID
        * admin -- the administration ID
        """
        if not url:
            url = 'https://moneybird.com/api/v2/'
        if not url.endswith('/'):
            url = url + '/'
        url = url + admin
        
        resty.client.Client.__init__(
            self,
            root=url,
            *arg,
            **kwarg
        )

    def request_hook(self, request):
        if not request.route.endswith('.json'):
            request.route = request.route + '.json'
