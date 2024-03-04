web: waitress-serve --port=${PORT:-5000} --trusted-proxy='*' --trusted-proxy-headers=x-forwarded-proto --asyncore-use-poll wsgi:application
