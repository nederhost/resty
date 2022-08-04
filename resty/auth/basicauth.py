import resty.auth.headerauth as headerauth
import base64

class Authorization(headerauth.Authorization):

    def __init__(self):
        headerauth.Authorization.__init__(self, type='Basic')

    def set_authorization(self, username, password):
        headerauth.Authorization.set_authorization(
          self,
          base64.b64encode('{0}:{1}'.format(username, password).encode())
        )
