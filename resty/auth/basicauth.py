import resty.auth.headerauth as headerauth
import base64

class Authorization(headerauth.Authorization):

    def set_authorization(self, username, password):
        headerauth.Authorization.set_authorization(self,
            type='Basic',
            token=base64.b64encode('{0}:{1}'.format(username, password).encode())
        )
        