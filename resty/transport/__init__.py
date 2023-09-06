import resty.base
import resty.client

class TransportBase(resty.base.ImplementationBase):
    
    def response(self, raw_response, headers=None):
        return resty.client.Response(raw_response, headers)
  