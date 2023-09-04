"""
Zammad API client

# Usage
```
import resty.api.zammad

client = resty.api.zammad.ZammadClient(url=zammad_url)
client.set_authorization('s3cr3tap1k3y')

# Optionally act as a specific user.
with client.on_behalf_of(user_email):
    client.api.tickets.post(title='new ticket', customer=user_email, article=article_data)

# Note that auth_customer is a custom field.
my_tickets = client.api.tickets.search.get(query='number:12345 AND auth_customer:56789')
```
"""

import resty.client
import resty.auth

class ZammadClient(resty.client.Client):
    """
    The Zammad API client.
    """

    def __init__(self, *arg, url, **kwarg):
        """
        Arguments in addition to those of the base class:
        * url -- the URL of the Zammad API to connect to
        """
        if not url.endswith('/'):
            url = url + '/'
        resty.client.Client.__init__(
            self,
            root=url,
            auth=resty.auth.headerauth.Authorization(type='Token', prefix='token='),
            *arg,
            **kwarg
        )
        self.__on_behalf_of = None
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, tb):
        self.__on_behalf_of = None
        
    def on_behalf_of(self, uid):
        """
        Set a specific UID for this client; meant to be used as a context
        manager.  This sets the Zammad-specific X-On-Behalf-Of header on any
        requests within the context.
        """
        self.__on_behalf_of = uid
        return self

    def request_hook(self, request):
        if self.__on_behalf_of:
            request.headers['X-On-Behalf-Of'] = self.__on_behalf_of
