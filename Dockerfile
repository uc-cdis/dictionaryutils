FROM quay.io/cdis/python-nginx:chore_rust_install

RUN pip install --upgrade pip
RUN apk add --update \
    postgresql-libs postgresql-dev libffi-dev libressl-dev \
    linux-headers musl-dev gcc g++ \
    curl bash git vim logrotate
RUN apk --no-cache add --update \
    aspell aspell-en ca-certificates \
    && mkdir -p /usr/share/dict/ \
    && aspell -d en dump master > /usr/share/dict/words

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
COPY . /src/
WORKDIR /src
RUN source $HOME/.poetry/env \
    && poetry config virtualenvs.create false \
    && poetry install -vv --no-interaction

COPY . /dictionaryutils

CMD cd /dictionary; rm -rf build dictionaryutils dist gdcdictionary.egg-info; python setup.py install --force && cp -r /dictionaryutils . && cd /dictionary/dictionaryutils; nosetests -s -v; export SUCCESS=$?; cd ..; rm -rf build dictionaryutils dist gdcdictionary.egg-info; exit $SUCCESS
