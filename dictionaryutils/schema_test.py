"""This is an example of json schema for the GDC using schemas defined
in local yaml files.

Included are a few functions to augment jsonschema and the python
validator.

Examples are at the end.

"""


import argparse
import copy
from gdcdictionary import gdcdictionary, SCHEMA_DIR
import glob
import json
from jsonschema import validate, ValidationError
import os
import re
import unittest
import yaml


def load_yaml_schema(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_project_specific_schema():
    project_path = os.path.join(CUR_DIR, "schemas/projects/")
    projects = {}
    if os.path.exists(project_path):
        for fp in os.listdir(project_path):
            path = os.path.join(project_path, fp)
            projects[fp.replace(".yaml", "")] = load_yaml_schema(path)
    return projects


CUR_DIR = os.path.dirname(SCHEMA_DIR)

DATA_DIR = os.path.join(CUR_DIR, "examples")
projects = load_project_specific_schema()


def merge_schemas(a, b, path=None):
    """Recursively zip schemas together

    """
    path = path if path is not None else []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_schemas(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                print(
                    "Overriding '{}':\n\t- {}\n\t+ {}".format(
                        ".".join(path + [str(key)]), a[key], b[key]
                    )
                )
                a[key] = b[key]
        else:
            print("Adding '{}':\n\t+ {}".format(".".join(path + [str(key)]), b[key]))
            a[key] = b[key]
    return a


def get_project_specific_schema(projects, project, schema, entity_type):
    """Look up the core schema for its type and override it with any
    project level overrides

    """
    root = copy.deepcopy(schema)
    project_overrides = projects.get(project)
    if project_overrides:
        overrides = project_overrides.get(entity_type)
        if overrides:
            merge_schemas(root, overrides, [entity_type])
    return root


def validate_entity(entity, schemata, project=None, name=""):
    """Validate an entity by looking up the core schema for its type and
    overriding it with any project level overrides

    """
    local_schema = get_project_specific_schema(
        projects, project, schemata[entity["type"]], entity["type"]
    )
    result = validate(entity, local_schema)
    return result


def validate_schemata(schemata, metaschema):
    # https://github.com/graphql-python/graphql-core-legacy/blob/v2.3.2/graphql/utils/assert_valid_name.py#L3
    graphql_name_regex = "^[_a-zA-Z][_a-zA-Z0-9]*$"
    compiled_regex = re.compile(graphql_name_regex)

    # validate schemata
    print("Validating schemas against metaschema...")
    for s in schemata.values():
        print("Validating '{}'".format(s.get("title")))
        validate(s, metaschema)

        def assert_link_is_also_prop(link):
            assert (
                link in s["properties"]
            ), "Entity '{}' has '{}' as a link but not property".format(s["id"], link)

        for link in [l["name"] for l in s["links"] if "name" in l]:
            assert_link_is_also_prop(link)
        for subgroup in [l["subgroup"] for l in s["links"] if "name" not in l]:
            for link in [l["name"] for l in subgroup if "name" in l]:
                assert_link_is_also_prop(link)

        for prop in s["properties"]:
            match = compiled_regex.match(prop)
            assert match, "prop name {} in {} does not match {}".format(
                prop, s["id"], graphql_name_regex
            )


class SchemaTest(unittest.TestCase):
    def setUp(self):
        self.dictionary = gdcdictionary
        self.definitions = yaml.safe_load(
            open(os.path.join(CUR_DIR, "schemas", "_definitions.yaml"), "r")
        )

    def test_schemas(self):
        validate_schemata(self.dictionary.schema, self.dictionary.metaschema)

    def test_valid_files(self):
        for path in glob.glob(os.path.join(DATA_DIR, "valid", "*.json")):
            print("Validating {}".format(path))
            doc = json.load(open(path, "r"))
            print(doc)
            if type(doc) == dict:
                self.add_system_props(doc)
                validate_entity(doc, self.dictionary.schema)
            elif type(doc) == list:
                for entity in doc:
                    self.add_system_props(entity)
                    validate_entity(entity, self.dictionary.schema)
            else:
                raise Exception("Invalid json")

    def test_invalid_files(self):
        for path in glob.glob(os.path.join(DATA_DIR, "invalid", "*.json")):
            print("Validating {}".format(path))
            doc = json.load(open(path, "r"))
            if type(doc) == dict:
                self.add_system_props(doc)
                with self.assertRaises(ValidationError):
                    validate_entity(doc, self.dictionary.schema)
            elif type(doc) == list:
                for entity in doc:
                    self.add_system_props(entity)
                    with self.assertRaises(ValidationError):
                        validate_entity(entity, self.dictionary.schema)
            else:
                raise Exception("Invalid json")

    def add_system_props(self, doc):
        schema = self.dictionary.schema[doc["type"]]
        for key in schema["systemProperties"]:
            use_def_default = (
                "$ref" in schema["properties"][key]
                and key in self.definitions
                and "default" in self.definitions[key]
            )
            if use_def_default:
                doc[key] = self.definitions[key]["default"]


if __name__ == "__main__":

    ####################
    # Setup
    ####################

    parser = argparse.ArgumentParser(description="Validate JSON")
    parser.add_argument(
        "jsonfiles",
        metavar="file",
        type=argparse.FileType("r"),
        nargs="*",
        help="json files to test if (in)valid",
    )

    parser.add_argument(
        "--invalid",
        action="store_true",
        default=False,
        help="expect the files to be invalid instead of valid",
    )

    args = parser.parse_args()

    ####################
    # Example validation
    ####################

    # Load schemata
    dictionary = gdcdictionary

    for f in args.jsonfiles:
        doc = json.load(f)
        if args.invalid:
            try:
                print(("CHECK if {0} is invalid:".format(f.name)), end=" ")
                print(type(doc))
                if type(doc) == dict:
                    validate_entity(doc, dictionary.schema)
                elif type(doc) == list:
                    for entity in doc:
                        validate_entity(entity, dictionary.schema)
                else:
                    raise ValidationError("Invalid json")
            except ValidationError as e:
                print("Invalid as expected.")
                pass
            else:
                raise Exception("Expected invalid, but validated.")
        else:
            print(("CHECK if {0} is valid:".format(f.name)), end=" ")
            if type(doc) == dict:
                validate_entity(doc, dictionary.schema)
            elif type(doc) == list:
                for entity in doc:
                    validate_entity(entity, dictionary.schema)
            else:
                print("Invalid json")

            print("Valid as expected")
    print("ok.")
