import os
import static
from wsgioauth2 import google

application = static.Cling('/app/docs/_build/html')

key = os.environ.get('DJANGO_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
secret = os.environ.get('DJANGO_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

client = google.make_client(client_id=key, client_secret=secret, hd="thermondo.de",
scope="https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile")
application = client.wsgi_middleware(application, secret=secret.encode('utf-8'))
