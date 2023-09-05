import resty.auth

class Authorization(resty.auth.AuthBase):

    def __init__(self, headername='Authorization', type='Bearer', prefix=None):
        self.headername = headername
        self.type = type
        self.prefix = prefix

    def add_authorization(self, request):
        request.headers[self.headername] = self.value

    def set_authorization(self, token):
        try:
            token = token.decode()
        except AttributeError:
            pass
        if self.prefix:
            token = f'{self.prefix}{token}'
        if self.type:
            self.value = '{0} {1}'.format(self.type, token)
        else:
            self.value = token
