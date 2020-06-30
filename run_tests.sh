#!/bin/bash
set -e

# Test if running under a dictionary/ folder
if [[ -d ../.git && -d ../gdcdictionary ]]; then
  (
    cd ..
    DICTCOMMIT=`git rev-parse HEAD` && echo "DICTCOMMIT=\"${DICTCOMMIT}\"" >dictionaryutils/dictionaryutils/version_data.py
    DICTVERSION=`git describe --always --tags` && echo "DICTVERSION=\"${DICTVERSION}\"" >>dictionaryutils/dictionaryutils/version_data.py
  )
fi

# Installing poetry using bootstrap script instead of pip install poetry to avoid any dependency conflicts. 
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

source $HOME/.poetry/env

which poetry

poetry install -v

# Here is a story. While updating data-simulator the new dependency was introduced there: gen3dictionary.
# And because this new dependency installed after the setup.py for testing the dictionary is run,
# it essentially tests gen3dictionary. :shrug:
# Removing if and only we're under `dictionary/` folder, essentially testing other dictionary.
if [[ -d ../.git && -d ../gdcdictionary ]]; then
  pip uninstall -y gen3dictionary
fi

nosetests -s -v
python bin/dump_schema.py
set +e
