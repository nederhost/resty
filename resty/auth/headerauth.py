import resty.auth

class Authorization(resty.auth.AuthBase):

    def __init__(self, headername='Authorization', type='Bearer'):
        self.headername = headername
        self.type = type

    def add_authorization(self, request):
        request.headers[self.headername] = self.value

    def set_authorization(self, token):
        try:
            token = token.decode()
        except AttributeError:
            pass
        if self.type:
            self.value = '{0} {1}'.format(self.type, token)
        else:
            self.value = token
