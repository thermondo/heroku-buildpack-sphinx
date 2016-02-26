import os

import requests
import static
from wsgi_sslify import sslify
from wsgioauth2 import Service

application = static.Cling('/app/docs/_build/html')

key = os.environ.get('GOOGLE_OAUTH2_KEY')
secret = os.environ.get('GOOGLE_OAUTH2_SECRET')


class GoogleService(Service):
    def __init__(self, allowed_domains=None):
        super().__init__(
            authorize_endpoint='https://accounts.google.com/o/oauth2/auth',
            access_token_endpoint='https://accounts.google.com/o/oauth2/token')
        # coerce a single string into a list
        if isinstance(allowed_domains, str):
            allowed_domains = allowed_domains.split(',')
        self.allowed_domains = allowed_domains

    def is_user_allowed(self, access_token):
        response = requests.get(
            'https://www.googleapis.com/oauth2/v1/tokeninfo',
            params={'access_token': access_token['access_token']},
            verify=True,
        )

        res = response.json()
        email = res['email']
        verified = res['verified_email']
        return any(
            email.endswith(allowed_domain)
            for allowed_domain in self.allowed_domains
        ) and verified


google = GoogleService(
    allowed_domains=os.environ.get('GOOGLE_ALLOWED_DOMAINS')
)


client = google.make_client(
    client_id=key,
    client_secret=secret,
    scope="email",
)


application = client.wsgi_middleware(application, secret=secret.encode('utf-8'), path='/oauth2/')
application = sslify(application, proxy_header='X-Forwarded-Proto')
