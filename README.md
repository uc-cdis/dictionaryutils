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


## Generate simulated data with Docker
If you wish to generate fake simulated data you can also do that with dictionaryutils and the data-simulator.

```
simdata() { docker run --rm -v $(pwd):/dictionary -v $(pwd)/simdata:/simdata quay.io/cdis/dictionaryutils:master /bin/sh -c "cd /dictionary && python setup.py install --force; python /src/datasimulator/bin/data-simulator simulate --path /simdata/ $*; export SUCCESS=$?; rm -rf build dictionaryutils dist gdcdictionary.egg-info; chmod -R a+rwX /simdata; exit $SUCCESS"; }
simdataurl() { docker run --rm -v $(pwd):/dictionary -v $(pwd)/simdata:/simdata quay.io/cdis/dictionaryutils:master /bin/sh -c "python /src/datasimulator/bin/data-simulator simulate --path /simdata/ $*; chmod -R a+rwX /simdata"; }

```

Then from the directory containing the `gdcdictionary` directory run `simdata` and a folder will be created called `simdata` with the results of the simulator run. You can also pass in additional arguments to the data-simulator script such as `simdata --max_samples 10`.

The `--max_samples` argument will define a default number of nodes to simulate, but you can override it using the `--node_num_instances_file` argument. For example, if you create the following `instances.json`:

```
{
        "case": 100,
        "demographic": 100
}

```
Then run the following:
```
docker run --rm -v $(pwd):/dictionary -v $(pwd)/simdata:/simdata quay.io/cdis/dictionaryutils:master /bin/sh -c "cd /dictionary && python setup.py install --force; python /src/datasimulator/bin/data-simulator simulate --path /simdata/ --program workshop --project project1 --max_samples 10 --node_num_instances_file instances.json; export SUCCESS=$?; rm -rf build dictionaryutils dist gdcdictionary.egg-info; chmod -R a+rwX /simdata; exit $SUCCESS";
```
Then you'll get 100 each of `case` and `demographic` nodes and 10 each of everything else. Note that the above example also defines `program` and `project` names.

You can also run the simulator for an arbitrary json url by using `simdataurl --url https://datacommons.example.com/schema.json`.


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
