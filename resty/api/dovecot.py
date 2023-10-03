"""
Dovecot API client.

# Usage
```
import resty.api.dovecot

client = resty.api.dovecot.DovecotClient(url='http://localhost:999/')
client.set_authorization('s3cr3tap1k3y')

quota = client.doveadm.quotaGet(user='username')
```

The Dovecot API client uses a doveadm attribute to provide the API instead
of the regular API attribute; this is due to the lack of actual paths on the
API.
"""

import base64

import resty.client
import resty.auth
import resty.exception

class DovecotClient(resty.client.Client):
    """
    The Dovecot API client.
    """

    def __init__(self, *arg, url, **kwarg):
        """
        Arguments in addition to those of the base class:
        * url -- the URL of the Dovecot API
        """
        if not url.endswith('/'):
            url = url + '/'
        url = url + 'doveadm/v1'
        
        resty.client.Client.__init__(
            self,
            root=url,
            auth=resty.auth.headerauth.Authorization(type='X-Dovecot-API'),
            *arg,
            **kwarg
        )
        self.doveadm = Doveadm(self)

    def set_authorization(self, api_key):
        return super().set_authorization(
          base64.b64encode(api_key.encode('utf-8')).decode('utf-8')
        )

    def serialize_hook(self, request):
        # The Dovecot API expects a three-element array (as provided by the
        # command() method below) and nothing else.
        request.parameters = request.positional


class Doveadm:

    def __init__(self, client):
        self._client = client
        
    def __getattr__(self, name):
        def command(_tag=None, **arguments):
            type, response, tag = self._client.api.post([name, arguments, _tag if _tag else name]).content[0]
            if type == 'error':
                raise resty.exception.ClientError(
                  client=client,
                  request=[name, arguments, _tag],
                  response=response,
                  msg=f"{response.get('exitCode', '')} {response.get('type', '')}",
                  status=response.get('exitCode', 0)
                )
            return response
        return command
