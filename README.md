# Sphinx Heroku Buildpack

[![Build Status](https://travis-ci.org/Thermondo/heroku-buildpack-sphinx.svg?branch=master)](https://travis-ci.org/Thermondo/heroku-buildpack-sphinx)
[![Latest Release](https://img.shields.io/github/tag/Thermondo/heroku-buildpack-sphinx.svg)](https://github.com/Thermondo/heroku-buildpack-sphinx/releases)

A Heroku buildpack to generate launch a sphinx documentation based on the same repository.

For more information read about [Heroku Buildpacks](https://devcenter.heroku.com/articles/buildpacks)

## Setting up Sphinx Heroku Buildpack

Setting up documentation with graphviz.

* Create heroku app to host sphinx documentation.

```shell
heroku create myapp-docs
```

The order of buildpacks on your application is important!

*  First setup heroku-buildpack-graphviz
```shell
heroku buildpacks:set https://github.com/weibeld/heroku-buildpack-graphviz.git
```

*  Setup sphinx-heroku-buildpack
```shell
heroku buildpacks:add --index 2 https://github.com/Thermondo/sphinx-heroku-buildpack.git
```

* Finally setup heroku's official python buildpack
```shell
heroku buildpacks:add --index 3 heroku/python
```

When listing the buildpacks on our application, we get this result:

```shell
heroku buildpacks --app myapp-docs
=== myapp-docs Buildpack URLs
1. https://github.com/weibeld/heroku-buildpack-graphviz.git     # If you need graphiz
2. https://github.com/Thermondo/heroku-buildpack-sphinx.git
3. heroku/python
```

## Why?

With Heroku auto deploy configured it reduces deployment time by serving sphinx documentation on a separate Heroku app but still using the same source code for your application. And allows to host private documentation.

##  Use Case

When using Heroku, Github and Travis:

```bash
git push {remotename} master
```

Your application `myapp` will be tested by travis and deployed regularly to Heroku, while sphinx documentation will be build and served on `myapp-docs` separately.


## Custom `wsgi.py` file

You can have a custom `wsgi.py` file to enable `oauth2` authentication and use `SSL`.


* Create a wsgi.py file in your docs folder
```shell
touch docs/wsgi.py
```

* Customize the `wsgi.py` file to authenticate user login using [wsgi-oauth2](https://github.com/dahlia/wsgi-oauth2) and [SSL](https://github.com/jacobian/wsgi-sslify).

```python
import os

import requests
import static
from wsgi_sslify import sslify
from wsgioauth2 import Service


class GoogleService(Service):
    def __init__(self, allowed_domains=None):
        super().__init__(
            authorize_endpoint='https://accounts.google.com/o/oauth2/auth',
            access_token_endpoint='https://accounts.google.com/o/oauth2/token')

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


key = os.environ.get('GOOGLE_OAUTH2_KEY')
secret = os.environ.get('GOOGLE_OAUTH2_SECRET')

google = GoogleService(allowed_domains=os.environ.get('GOOGLE_ALLOWED_DOMAINS'))

client = google.make_client(client_id=key, client_secret=secret, scope="email")

application = static.Cling('/app/docs/_build/html')
application = client.wsgi_middleware(application, secret=secret.encode('utf-8'), path='/oauth2/')
application = sslify(application, proxy_header='X-Forwarded-Proto')

```

## Custom `post_compile` file

* Create a post_compile file in your docs folder
```shell
touch docs/post_compile
```

* Customize your post_compile

```shell
...
Your custom commands
...

pip install -r ${BUILD_DIR}/docs/requirements.txt

# Build Sphinx documentation
(cd ${BUILD_DIR}/docs && make apidoc html)
```
