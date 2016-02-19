import os
import static
import requests
from wsgioauth2 import github

application = static.Cling('/app/docs/_build/html')

key = os.environ.get('GITHUB_OAUTH2_CLIENT_ID')
secret = os.environ.get('GITHUB_OAUTH2_CLIENT_SECRET')

client = github.make_client(client_id=key, client_secret=secret)
application = client.wsgi_middleware(application, secret=secret.encode('utf-8'))
