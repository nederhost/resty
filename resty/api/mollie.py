import resty.client
import resty.data.xml.elementtree
import resty.auth
import resty.auth.basicauth as basicauth

class MollieClient(resty.client.Client):

    def __init__(self, *arg, url='https://api.mollie.nl/v2', **kwarg):
        resty.client.Client.__init__(
            self, 
            root=url,
            *arg,
            **kwarg
        )
