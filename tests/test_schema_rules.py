from dictionaryutils import dictionary


def test_no_mixed_type_in_enum():
    for schema in dictionary.schema.values():
        for prop in schema["properties"].values():
            if "enum" in prop:
                assert all(
                    [type(i) == str for i in prop["enum"]]
                ), "{}: enum values should all be string".format(schema["id"])


def test_lowercase_ids():
    for schema in dictionary.schema.values():
        if "id" in schema:
            assert (
                schema["id"] == schema["id"].lower()
            ), "The id in {} should be lower case".format(schema["id"])
