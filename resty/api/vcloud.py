"""
VMWare vCloud Directory API client.

# Usage

```
import resty.api.vcloud

vdc_name = 'My_OrgVDC'
vapp_name = 'My VApp'

client = resty.api.vcloud.vCloudClient('https://example.nl/api')
client.set_authorization('username', 'Organisation', 's3cr3t')

vdc = client.filter(client.route('query').get(type='orgVdc').record, {'name': vdc_name})[0]
vapp = client.filter(client.route('vApps/query').get().record, {'name': vapp_name})[0]
disk = client.filter(client.route('query').get(type='disk').record, {'name': 'mydisk'})[0]
"""
#pylint: disable=bad-continuation

import resty.client
import resty.auth
import resty.auth.basicauth as basicauth

class VCloudClient(resty.client.Client):
    """
    VMWARE vCloud Director API client.
    """

    def __init__(self, *arg, api_version='34.0', **kwarg):
        """
        Arguments in addition to those of the base class:
        * api_version -- the API version to be used
        """
        resty.client.Client.__init__(
          self,
          *arg,
          auth=resty.api.vcloud.Auth(),
          **kwarg
        )
        self.api_version = api_version

    def serialize_hook(self, request): # pylint: disable=no-self-use
        """
        vCloud requires a specific media type to be specified for POST requests.
        """
        if request.method == 'POST' and request.positional:
            request.headers['Content-Type'] = request.positional[0]

    def request_hook(self, request):
        """
        vCloud requires application/*+json to be listed in the Accept header
        to return JSON formatted responses.
        """
        request.headers['Accept'] = 'application/*+json;version={0}'.format(self.api_version)

    def filter(self, objects, filter_=None, type_=None): # pylint: disable=no-self-use
        """
        Filter returned objects by type or other properties.

        Arguments:
        * objects -- the record attribute of the objects as returned by the
          get() method
        * filter_ -- a dictionary containing property names which should
          match
        * type_ -- the name of a vCloud object type to be expected; this is
          the TYPE part in the application/vnd.vmware.TYPE+json content type
          or the full content type (both are supported)
        """
        filtered = []
        if type_ is not None:
            if not type_.startswith('application/'):
                if not type_.startswith('vnd.vmware'):
                    type_ = 'vnd.vmware.' + type_
                type_ = 'application/' + type_
            if not type_.endswith('+json'):
                type_ = type_ + '+json'
        for object_ in objects:
            if type_ is None or object_['type'] == type_:
                if (
                  filter_ is None or
                  all(k in object_ and object_[k] == v for (k, v) in filter_.items())
                ):
                    filtered.append(object_)
        return filtered

    def object_route(self, object_):
        """
        Return a route to a specific object.
        """
        return self.route(object_['href'])


class Auth(resty.auth.AuthBase):
    """
    vCloud specific authentication handling.

    A first call is made with HTTP Basic Authentication and the provided
    username, organisation name and password to get a token; the token is
    then used for the rest of the requests.
    """

    def __init__(self):
        self.basicauth = None
        self.token = None

    def add_authorization(self, request):
        """
        Add the correct type of authorization to the request.
        """
        if self.token:
            request.headers['Authorization'] = self.token
        elif self.basicauth:
            self.basicauth.add_authorization(request)

    def set_authorization(self, username, organization, password):
        """
        Authenticate and retrieve a session token.

        Arguments:
        * username -- the API username
        * organization -- the API organization name
        * password -- the API password

        For basic authentication the username and organization name are
        joined with the '@' as per vCloud's API specification.
        """
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

# An earlier version of this API spelled it differently.  This is for
# backwards compatibility.
vCloudClient = VCloudClient # pylint: disable=invalid-name
