import resty.auth

class Authorization(resty.auth.AuthBase):

    def add_authorization(self, request):
        request.headers[self.headername] = self.value
        
    def set_authorization(self, token, headername='Authorization', type='Bearer'):
        self.headername = headername
        try:
            token = token.decode()
        except AttributeError:
            pass
        if type:
            self.value = '{0} {1}'.format(type, token)
        else:
            self.value = token
            