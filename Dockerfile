FROM python:2.7-alpine

RUN apk --no-cache add \
        ca-certificates \
        gcc \
	git \
        libffi-dev \
        musl-dev \
        postgresql-dev \
    && pip install --upgrade pip

COPY . /dictionaryutils

RUN pip install -r /dictionaryutils/dev-requirements.txt

CMD cd /dictionary && python setup.py install --force && cp -r /dictionaryutils . && cd /dictionary/dictionaryutils && nosetests -s -v
