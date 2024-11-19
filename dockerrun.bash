#!/bin/bash

# This script sets up the poetry environment for running tests
# against a local build of a dictionary repo.
# This will remove the default gdcdictionary (eg, version 2.0.0)
# and install the local dictionary (eg, version 0.0.0).
#
# Similar to
# https://github.com/uc-cdis/.github/blob/master/.github/workflows/dictionary_push.yaml

cd /dictionary
if [ -f pyproject.toml ]; then
    export USE_POETRY=1
else
    export USE_POETRY=0
fi
# TODO: remove after testing
echo "Use poetry ${USE_POETRY}"

echo "Removing old dictionaryutils"
rm -rf build dictionaryutils dist gdcdictionary.egg-info

echo "Installing dictionary"
if [ $USE_POETRY -eq 1 ]; then
  echo "Via poetry"
  poetry install -v --all-extras --no-interaction || true
fi

cp -r /dictionaryutils .
cd /dictionary/dictionaryutils

echo "Removing old gdcdictionary"
if [ $USE_POETRY -eq 1 ]; then
  poetry run pip uninstall -y gen3dictionary
  poetry run pip uninstall -y gdcdictionary
else
  poetry remove gdcdictionary
  poetry run pip uninstall -y gen3dictionary
fi

echo "Reinstall dictionary"
poetry run pip install ..

poetry show

echo "The following schemas from dictionary will be tested:"
ls `poetry run python -c "from gdcdictionary import SCHEMA_DIR; print(SCHEMA_DIR)"`

echo "Ready to run tests"
poetry run pytest -v tests
export SUCCESS=$?
echo "Success = ${SUCCESS}"

# TODO: remove after testing
echo "Ready to dump schema"
poetry run python bin/dump_schema.py
echo "Number of schemas in artifact"
grep -o ".yaml\"" artifacts/schema.json | wc -l

echo "Clean up"
rm -rf build dictionaryutils dist gdcdictionary.egg-info

exit $SUCCESS
