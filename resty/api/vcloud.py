import resty.client
import resty.auth
import resty.auth.basicauth as basicauth

class vCloudClient(resty.client.Client):

    def __init__(self, *arg, api_version='34.0', **kwarg):
        resty.client.Client.__init__(
            self, 
            *arg,
            auth=resty.api.vcloud.Auth(),
            **kwarg
        )
        self.api_version = api_version
        
    # vCloud requires a specific media type to be specified for POST requests
    def serialize_hook(self, request):
        if request.method == 'POST' and request.positional:
            request.headers['Content-Type'] = request.positional[0]
        
    def request_hook(self, request):
        request.headers['Accept'] = 'application/*+json;version={0}'.format(self.api_version)

    def filter(self, objects, filter=None, type=None):
        filtered = []
        if type is not None:
            if not type.startswith('application/'):
                if not type.startswith('vnd.vmware'):
                    type = 'vnd.vmware.' + type
                type = 'application/' + type
            if not type.endswith('+json'):
                type = type + '+json'
        for object in objects:
            if type is None or object['type'] == type:
                if filter is None or all (k in object and object[k] == v for (k, v) in filter.items()):
                    filtered.append(object)
        return filtered
        
    def object_route(self, object):
        return self.route(object['href'])

#
# On setting the authorization information we do a call to a URL with HTTP
# Basic Authentication to get a token; the token is used in the rest of the
# requests.
        
class Auth(resty.auth.AuthBase):

    def __init__(self):
        self.basicauth = None
        self.token = None

    def add_authorization(self, request):
        if self.token:
            request.headers['Authorization'] = self.token
        elif self.basicauth:
            self.basicauth.add_authorization(request)

    def set_authorization(self, username, organization, password):
        # Get the URL we should use for logging in.
#        response = self.client.route('sessions').get()
        # We use HTTP Basic Auth to get a session token that is used for
        # subsequent requests.
        self.basicauth = basicauth.Authorization()
        self.basicauth.set_client(self.client)
        self.basicauth.set_authorization(
            username='{0}@{1}'.format(username, organization),
            password=password
        )
        response = self.client.route('sessions').post()
        if 'x-vmware-vcloud-access-token' in response.headers:
            self.token = '{0} {1}'.format(
              response.headers['x-vmware-vcloud-token-type'],
              response.headers['x-vmware-vcloud-access-token']
            )
        else:
            raise resty.exception.AuthenticationFailed(self.client)
