FROM python:2.7

RUN pip install --upgrade pip

COPY . /dictionaryutils

RUN pip install -r /dictionaryutils/dev-requirements.txt

CMD cd /dictionary && python setup.py install --force && cp -r /dictionaryutils . && cd /dictionary/dictionaryutils && nosetests -s -v
