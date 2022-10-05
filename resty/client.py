import sys

import resty.exception
import resty.data.json
import resty.auth.headerauth
import resty.transport.url

class Client:

    def __init__(
        self,
        root,
        serializer=resty.data.json.Serializer(),
        parser=resty.data.json.Parser(),
        auth=resty.auth.headerauth.Authorization(),
        transport=resty.transport.url.Transport(),
        debuglevel=0,
        **kwargs
    ):
        self.root = root if root else ''
        self.serializer = serializer
        self.parser = parser
        self.auth = auth
        self.transport = transport
        if self.serializer:
            self.serializer.set_client(self)
        if self.parser:
            self.parser.set_client(self)
        if self.auth:
            self.auth.set_client(self)
        if self.transport:
            self.transport.set_client(self)
        self.debuglevel = debuglevel
        self.configuration = kwargs
        self.session = {}
        self.api = self.route(self.root)

    def debuginfo(self, msg, marker='-'):
        if marker:
            msg = "{0} {1} {0}\n{2}\n{0}\n".format(
                marker * 3,
                self,
                msg
            )
        print(msg, file=sys.stderr)

    def execute(self, request):

        # Update the request to add any necessary authorization information.
        if hasattr(self, 'auth_hook'): self.auth_hook(request)
        self.auth.add_authorization(request)

        # Serialize the request parameters. This should fill the
        # 'serialized' attribute.
        if hasattr(self, 'serialize_hook'): self.serialize_hook(request)
        if request.parameters is not None:
            self.serializer.serialize(request)

        # Execute the request.
        if hasattr(self, 'request_hook'): self.request_hook(request)
        if self.debuglevel > 1: self.debuginfo(request, '>')
        response = self.transport.process_request(request)
        if self.debuglevel > 1: self.debuginfo(response, '>')
        if hasattr(self, 'response_hook'): self.response_hook(response, request)

        # Replace the 'response' element with a parsed version.
        if response.raw_response:
            try:
                self.parser.parse(response)
            except Exception as e:
                raise resty.exception.ParseError(self, request, response) from e
        if hasattr(self, 'parse_hook'): self.parse_hook(response, request)

        return response

    def route(self, route='', always_relative=False):
        if always_relative or not route.startswith(self.root):
            return Route(self, '/'.join([self.root, route]))
        else:
            return Route(self, route)

    def set_authorization(self, *args, **kwargs):
        self.auth.set_authorization(*args, **kwargs)

class Route:

    def __init__(self, client, route):
        self.client = client
        self._route = route

    def __getattr__(self, name):
        # This makes stuff like some_object.some_subresource.method.post() work.
        return self.route(name)

    def __str__(self):
        return 'Route {0} via {1}'.format(self._route, self.client)

    def _execute(self, method, positional=None, parameters=None):
        if not positional: positional = None
        if not parameters: parameters = None
        return self.client.execute(Request(method, self._route, positional, parameters))

    def delete(self, *args, **kwargs):
        return self._execute('DELETE', args, kwargs)

    def delete_item(self, _item, *args, **kwargs):
        return self.route(_item, always_relative=True).execute('DELETE', args, kwargs)

    def get(self, *args, **kwargs):
        return self._execute('GET', args, kwargs)

    def get_item(self, _item, *args, **kwargs):
        return self.route(_item, always_relative=True).execute('GET', args, kwargs)

    def patch(self, *args, **kwargs):
        return self._execute('PATCH', args, kwargs)

    def patch_item(self, _item, *args, **kwargs):
        return self.route(_item, always_relative=True).execute('PATCH', args, kwargs)

    def put(self, *args, **kwargs):
        return self._execute('PUT', args, kwargs)

    def put_item(self, _item, *args, **kwargs):
        return self.route(_item, always_relative=True).execute('PUT', args, kwargs)

    def post(self, *args, **kwargs):
        return self._execute('POST', args, kwargs)

    def post_item(self, _item, *args, **kwargs):
        return self.route(_item, always_relative=True).execute('POST', args, kwargs)

    def route(self, route, always_relative=False):
        return Route(self.client, self._route + '/' + route)

class Request:

    def __init__(self, method, route, positional, parameters, headers={}):
        self.method = method
        self.route = route
        self.positional = positional
        self.parameters = parameters
        self.headers = headers
        self.data = None

    def __str__(self):
        m = '{0} {1}'.format(self.method, self.route)
        if self.headers:
            m += "\n" + "\n".join([ '{0}: {1}'.format(h, self.headers[h]) for h in self.headers]) + "\n"
        if self.data:
            m += "\n" + self.data
        return m

    def set_data(self, data, contenttype):
        self.data = data
        if 'content-type' not in [h.lower() for h in self.headers]:
            self.headers['Content-Type'] = contenttype

class Response:

    def __init__(self, raw_response, headers={}):
        self.raw_response = raw_response
        self.headers = headers
        self.content = None

    # Make any response fields that does not clash with the builtins available as attributes.
    def __getattr__(self, name):
        try:
            return self.content[name]
        except:
            raise AttributeError

    def __str__(self):
        m = ''
        if self.headers:
            m += "\n".join([ '{0}: {1}'.format(h, self.headers[h]) for h in self.headers]) + "\n\n"
        m += self.raw_response
        return m
