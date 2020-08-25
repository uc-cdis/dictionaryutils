FROM python:3.6-alpine

RUN apk --no-cache add \
        aspell \
        aspell-en \
        ca-certificates \
        gcc \
	git \
        libffi-dev \
        musl-dev \
        postgresql-dev \
    && pip install --upgrade pip \
    && mkdir -p /usr/share/dict/ \
    && aspell -d en dump master > /usr/share/dict/words

RUN pip install poetry==1.0.0
COPY . /src/
WORKDIR /src
RUN python -m venv /env && . /env/bin/activate && poetry install

COPY . /dictionaryutils

CMD cd /dictionary; rm -rf build dictionaryutils dist gdcdictionary.egg-info; python setup.py install --force && cp -r /dictionaryutils . && cd /dictionary/dictionaryutils; nosetests -s -v; export SUCCESS=$?; cd ..; rm -rf build dictionaryutils dist gdcdictionary.egg-info; exit $SUCCESS
