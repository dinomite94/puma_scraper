FROM python:3-alpine

ADD . /puma
WORKDIR /puma
VOLUME [ "/puma/out" ]

RUN apk add build-base libffi-dev libxml2-dev libxslt-dev openssl-dev --no-cache && \
    pip install -r requirements.txt && \
    apk del build-base

CMD ["python", "cli.py", "run"]
