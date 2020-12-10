import resty.exception
import resty.transport

import re
import urllib.error
import urllib.request

class Transport(resty.transport.TransportBase):

    default_charset = 'iso-8859-1'

    RE_charset = re.compile('; charset=(\S+)')

    def process_request(self, request):
        url = request.route
        if (request.route.startswith('http://') or request.route.startswith('https://')) and request.method == 'GET':
            # Special handling for HTTP GET requests: make sure all request
            # parameters are added to the URL and remove any post body as
            # that is not allowed with a GET request.
            if request.parameters:
                url += '?' + urllib.parse.urlencode(request.parameters)
                request.data = None
        if request.data:           
            m = self.RE_charset.match(request.headers['Content-Type'])
            if m:
                body = request.data.encode(m.group(1))
            else:
                body = request.data.encode(self.default_charset)
        else:
            body = None
        if body is None: 
            try:
                del request.headers['Content-Type']
                del request.headers['Content-Length']
                del request.headers['content-type']
                del request.headers['content-length']
            except KeyError:
                pass
        urlrequest = urllib.request.Request(url, body, request.headers, method=request.method)
        if self.client.debuglevel > 0: self.client.debuginfo(self._urlrequest_as_string(urlrequest), '>')
        try:
            urlresponse = urllib.request.urlopen(urlrequest)
        except urllib.error.HTTPError as e:
            if e.code == 401:
                exception_class = resty.exception.AuthenticationFailed
            elif e.code == 403:
                exception_class = resty.exception.AccessDenied
            elif e.code == 404:
                exception_class = resty.exception.NotFound
            elif e.code < 500:
                exception_class = resty.exception.ClientError
            else:
                exception_class = resty.exception.ServerError
            raise exception_class(self.client, request, msg=e.reason, status=e.code)
        data = urlresponse.read()
        if self.client.debuglevel > 0: self.client.debuginfo(self._urlresponse_as_string(urlresponse, data), '<')

        # Process the headers        
        headers = {}
        for (h, v) in urlresponse.getheaders():
            h = h.lower()
            if h in headers:
                if not isinstance(headers[h], list):
                    headers[h] = [ headers[h] ]
                headers[h].append(v)
            else:
                headers[h] = v
        headers['_status'] = urlresponse.status
                
        # Determine the character set and decode the content accordingly.
        charset = self.default_charset
        if 'content-type' in headers:
            m = re.match(headers['content-type'], '; charset=(\S+)')
            if m: 
                charset = m.group(1)
            elif re.match(headers['content-type'], '.+/xml'):
                m = re.match(data, '^<?xml[^>]*\sencoding="([^"]+)"')
                if m:
                    charset = m.group(1)
        if charset:
            data = data.decode(charset)
        response = resty.client.Response(data, headers);
        return response
    
    def _urlrequest_as_string(self, urlrequest):
        return "{0} {1}\n{2}\n\n{3}".format(
            urlrequest.method, 
            urlrequest.full_url,
            "\n".join([ '{0}: {1}'.format(h, v) for (h, v) in urlrequest.header_items()]),
            urlrequest.data.decode() if urlrequest.data else ''
        )
        
    def _urlresponse_as_string(self, urlresponse, data):
        return "{0} {1}\n{2}{3}".format(
            urlresponse.status,
            urlresponse.reason,
            urlresponse.headers,
            data.decode()
        )
             