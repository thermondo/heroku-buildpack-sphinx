
FROM heroku/heroku:16-build

WORKDIR /app


RUN mkdir -p /app/builds /var/env /tmp/build-cache /tmp/sphinx-heroku-buildpack /app/docs
RUN echo "pip" > /app/requirements.txt

RUN curl -sLo- https://github.com/heroku/heroku-buildpack-python/archive/master.tar.gz | tar xzf - -C /tmp

RUN curl -sLo- https://s3.amazonaws.com/assets.heroku.com/heroku-client/heroku-client.tgz | tar xzf - -C /opt
RUN ln -s /opt/heroku-client/bin/heroku /usr/bin/heroku
RUN heroku --version

COPY . /tmp/sphinx-heroku-buildpack
COPY ./test/docs /app/docs

RUN echo "\necho-build-dir:\n\t@echo '\$(BUILDDIR)'" >> docs/Makefile
RUN (cd /app/docs && make echo-build-dir > /app/docs/.build-dir)

RUN /tmp/sphinx-heroku-buildpack/bin/compile /app /var/env /tmp/build-cache

RUN /tmp/heroku-buildpack-python-master/bin/compile /app /var/env /tmp/build-cache

CMD PATH=.heroku/python/bin:$PATH heroku local
