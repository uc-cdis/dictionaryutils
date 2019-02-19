# dictionaryutils
python wrapper and metaschema for datadictionary.
It can be used to:
- load a local dictionary to a python object.
- dump schemas to a file that can be uploaded to s3 as an artifact.
- load schema file from an url to a python object that can be used by services

## Test for dictionary validity with Docker
Say you have a dictionary you are building locally and you want to see if it will pass the tests.

You can add a simple alias to your `.bash_profile` to enable a quick test command:
```
testdict() { docker run --rm -v $(pwd):/dictionary quay.io/cdis/dictionaryutils:master; }
```

Then from the directory containing the `gdcdictionary` directory run `testdict`.

## Use dictionaryutils to load a dictionary
```
from dictionaryutils import DataDictionary

dict_fetch_from_remote = DataDictionary(url=URL_FOR_THE_JSON)

dict_loaded_locally = DataDictionary(root_dir=PATH_TO_SCHEMA_DIR)
```

## Use dictionaryutils to dump a dictionary
```
import json
from dictionaryutils import dump_schemas_from_dir

with open('dump.json', 'w') as f:
    json.dump(dump_schemas_from_dir('../datadictionary/gdcdictionary/schemas/'), f)
```
