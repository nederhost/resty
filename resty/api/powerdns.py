"""
PowerDNS API client.

# Usage
```
import resty.api.powerdns

client = resty.api.powerdns.PowerDNSClient(url='http://localhost:8081/api/v1', server='localhost')
client.set_authorization('s3cr3tap1k3y')

zone = client.api.server.zones('12345').get()
```
"""

import resty.client
import resty.auth

class PowerDNSClient(resty.client.Client):
    """
    The PowerDNS API client.
    """

    def __init__(self, *arg, url, server='localhost', **kwarg):
        """
        Arguments in addition to those of the base class:
        * url -- the URL of the PowerDNS API
        * server -- the server name to use
        """
        if not url.endswith('/'):
            url = url + '/'
        url = url + 'servers/' + server
        
        resty.client.Client.__init__(
            self,
            root=url,
            auth=resty.auth.headerauth.Authorization(headername='X-API-Key', type=None),
            *arg,
            **kwarg
        )

    def request_hook(self, request):
        request.headers['Accept'] = 'application/json'
        
    def serialize_hook(self, request):
        # POST, PATCH and PUT requests take a single positional argument
        if request.method in ('PUT', 'POST', 'PATCH') and request.positional and len(request.positional) == 1:
            request.parameters = request.positional[0]
            request.positional = None
