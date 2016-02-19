import os
import static
import requests
from wsgioauth2 import Service

class GoogleService(Service):

    def __init__(self, allowed_orgs=None):
        super().__init__(
            authorize_endpoint='https://accounts.google.com/o/oauth2/auth',
            access_token_endpoint='https://accounts.google.com/o/oauth2/token')
        # coerce a single string into a list
        if isinstance(allowed_orgs, str):
            allowed_orgs = [allowed_orgs]
        self.allowed_orgs = allowed_orgs
        print('Print from __init__')

    def is_user_allowed(self, access_token):
        response = requests.get(
            'https://www.googleapis.com/oauth2/v1/tokeninfo',
            params={'access_token': access_token},
            verify=True,
        )
        print('Print form is_user_allowed')
        print('Token is:')
        print(access_token)

        print(response.text)
        print(response.json)

        # if response.status_code == 200:
        #
        #     return True
        # else:
        #     return False
        #

        return True

google = GoogleService(allowed_orgs='thermondo.de')

application = static.Cling('/app/docs/_build/html')

key = os.environ.get('DJANGO_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
secret = os.environ.get('DJANGO_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

client = google.make_client(
    client_id=key,
    client_secret=secret,
    hd="thermondo.de",
    scope="https://www.googleapis.com/auth/userinfo.email")

application = client.wsgi_middleware(application, secret=secret.encode('utf-8'), path='/oauth2/')
