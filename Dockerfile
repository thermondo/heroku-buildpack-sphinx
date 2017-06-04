
FROM heroku/heroku:16-build

WORKDIR /app

ENV STACK=heroku-16

RUN mkdir -p /app/builds /var/env /var/build-cache /tmp/sphinx-heroku-buildpack /app/docs

# Install heroku cli
RUN curl -sLo- https://s3.amazonaws.com/assets.heroku.com/heroku-client/heroku-client.tgz | tar xzf - -C /opt
RUN ln -s /opt/heroku-client/bin/heroku /usr/bin/heroku
RUN heroku --version

# Setup Sphinx test docs
COPY . /tmp/sphinx-heroku-buildpack
COPY ./test/docs /app/docs

# Setup fake heroku Python app
RUN echo "pip" > /app/requirements.txt

# Install Graphviz buildpack
RUN curl -sLo- https://github.com/weibeld/heroku-buildpack-graphviz/archive/master.tar.gz | tar xzf - -C /tmp
RUN /tmp/heroku-buildpack-graphviz-master/bin/compile /app /var/env /var/build-cache

# Install Sphinx buildpack
RUN /tmp/sphinx-heroku-buildpack/bin/compile /app /var/env /var/build-cache


# Install heroku/python buildpack
RUN curl -sLo- https://github.com/heroku/heroku-buildpack-python/archive/master.tar.gz | tar xzf - -C /tmp
RUN /tmp/heroku-buildpack-python-master/bin/compile /app /var/env /var/build-cache

CMD PATH=.heroku/python/bin:$PATH heroku local
