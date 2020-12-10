class BaseException(Exception):
  
    def __init__(self, client, request=None, response=None, msg=None, status=None):
        self.client = client
        self.request = request
        self.response = response
        self.status = status
        self.msg = msg
        
    def __str__(self):
        method = ''
        route = ''
        try:
            method = self.request.method
            route = self.request.route
        except Exception:
            pass
        return '{0} "{1}" while executing {2} {3}'.format(
            getattr(self, 'status', self.__class__.__name__),
            getattr(self, 'msg', ''),
            method,
            route
        )
        
class ParseError(BaseException):
    pass

class OperationalException(BaseException):
    # The group of exceptions that can be expected in "normal" operation.
    pass

class ClientError(OperationalException):
    pass

class AuthenticationFailed(ClientError):
    pass
     
class NotFound(ClientError):
    pass
    
class AccessDenied(ClientError):
    pass
