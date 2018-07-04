#!/bin/bash
set -e
cd ..
DICTCOMMIT=`git rev-parse HEAD` && echo "DICTCOMMIT=\"${DICTCOMMIT}\"" >dictionaryutils/dictionaryutils/version_data.py
DICTVERSION=`git describe --always --tags` && echo "DICTVERSION=\"${DICTVERSION}\"" >>dictionaryutils/dictionaryutils/version_data.py
cd dictionaryutils
pip uninstall -y dictionaryutils
python setup.py install --force
pip install -r dev-requirements.txt
nosetests -v
python bin/dump_schema.py
set +e
