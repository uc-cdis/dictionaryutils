FROM quay.io/cdis/python-nginx:pybase3-1.5.0

RUN pip install --upgrade pip
RUN apk add --update \
    postgresql-libs postgresql-dev libffi-dev libressl-dev \
    linux-headers musl-dev gcc g++ \
    curl bash git vim logrotate
RUN apk --no-cache add --update \
    aspell aspell-en ca-certificates \
    && mkdir -p /usr/share/dict/ \
    && aspell -d en dump master > /usr/share/dict/words

COPY . /src/
WORKDIR /src

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install -vv --no-interaction

COPY . /dictionaryutils

CMD cd /dictionary; rm -rf build dictionaryutils dist gdcdictionary.egg-info; python setup.py install --force && cp -r /dictionaryutils . && cd /dictionary/dictionaryutils; pip uninstall -y gen3dictionary; pytest tests -s -v; export SUCCESS=$?; cd ..; rm -rf build dictionaryutils dist gdcdictionary.egg-info; exit $SUCCESS
