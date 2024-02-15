class BaseException(Exception):

    def __init__(self, client, request=None, response=None, msg=None, status=None, content=None):
        self.client = client
        self.request = request
        self.response = response
        self.status = status
        self.msg = msg
        self.content = content

    def __str__(self):
        t = '{0} "{1}"'.format(
          getattr(self, 'status', self.__class__.__name__),
          getattr(self, 'msg', ''),
        )
        try:
            if self.request:
                t = t + f' during {self.request}'
        except AttributeError:
            pass
        return t
        
    __repr__ = __str__

class ParseError(BaseException):
    pass

class OperationalException(BaseException):
    # The group of exceptions that can be expected in "normal" operation.
    pass

class ServerError(OperationalException):
    pass

class ClientError(OperationalException):
    pass

class AuthenticationFailed(ClientError):
    pass

class NotFound(ClientError):
    pass

class AccessDenied(ClientError):
    pass
