from contextlib import contextmanager
import glob
import os
import yaml
from dictionaryutils import dictionary
from gdcdictionary import SCHEMA_DIR


def test_required_nodes():
    required_nodes = ["program", "project"]
    for node in required_nodes:
        assert (
            node in dictionary.schema
        ), "{} is a required node but not in the dictionary".format(node)


def test_required_data_fields():
    defined_fields = ["data_type", "data_format", "data_category", "object_id"]
    required_fields = ["data_type", "data_format", "data_category"]
    invalid_defined = []
    invalid_required = []
    for schema in dictionary.schema.values():
        if schema["category"].endswith("_file"):
            for field in defined_fields:
                if field not in schema["properties"]:
                    invalid_defined.append("{}: {}".format(schema["id"], field))
                else:
                    if field in required_fields and field not in schema["required"]:
                        invalid_required.append("{}: {}".format(schema["id"], field))
    assert (
        not invalid_defined
    ), "Fields should be required but are not defined in schema: {}".format(
        invalid_defined
    )
    assert (
        not invalid_required
    ), "Fields should be required but are not required in schema: {}".format(
        invalid_required
    )


def test_required_project_fields():
    required_fields = [
        "availability_type",
        "code",
        "dbgap_accession_number",
        "id",
        "type",
    ]
    schema = dictionary.schema["project"]
    for field in required_fields:
        assert field in schema["properties"], "{} is required for project".format(field)


def test_required_program_fields():
    required_fields = ["id", "type"]
    schema = dictionary.schema["program"]
    for field in required_fields:
        assert field in schema["properties"], "{} is required for program".format(field)


def test_required_ubiquitous_fields():
    required_fields = [
        "updated_datetime",
        "created_datetime",
        "id",
        "type",
        "submitter_id",
    ]
    for schema in dictionary.schema.values():
        if (
            not schema["id"] == "program"
            and not schema["id"] == "project"
            and not schema["category"] == "internal"
        ):
            for field in required_fields:
                assert (
                    field in schema["properties"]
                ), "{} is required but not in {}".format(field, schema["id"])


def test_id_matches():
    # file names must match id files...
    @contextmanager
    def visit_directory(path):
        cdir = os.getcwd()
        try:
            os.chdir(path)
            yield os.getcwd()
        finally:
            os.chdir(cdir)

    def load_yaml(name):
        with open(name, "r") as f:
            return yaml.safe_load(f)

    with visit_directory(SCHEMA_DIR):
        for path in glob.glob("*.yaml"):
            filename = os.path.splitext(path)[0]
            schema = load_yaml(path)
            if "id" in schema:
                assert filename == schema["id"], "{} file has unmatched id {}".format(
                    path, schema["id"]
                )


def test_enums_dont_have_type():
    """
    When a property is of type "enum", the "type" field should not
    be specified.
    Checking this avoids bugs when using the data simulator: it uses the
    "type" field to decide which type of data to simulate when "type" is
    specified. When it's not specified, it falls back on the type of the
    "enum" values.
    """
    for schema in dictionary.schema.values():
        props = schema.get("properties", {})
        for prop_id, prop_details in props.items():
            if "enum" in prop_details:
                assert (
                    "type" not in prop_details
                ), 'Property "{}" of node "{}" is an enum, so field "type" should not be specified.'.format(
                    prop_id, schema["id"]
                )


def test_arrays_have_items():
    for schema in dictionary.schema.values():
        props = schema.get("properties", {})
        for prop_id, prop_details in props.items():
            if prop_details.get("type") == "array":
                assert (
                    "items" in prop_details
                ), 'Property "{}" of node "{}" is of type "array", so field "items" should be specified.'.format(
                    prop_id, schema["id"]
                )


def test_file_size_is_integer():
    for schema in dictionary.schema.values():
        props = schema.get("properties", {})
        if "file_size" in props:
            t = props["file_size"].get("type")
            assert (
                t == "integer"
            ), 'Property "file_size" of node "{}" should be of type "integer", but is of type "{}".'.format(
                schema["id"], t
            )
