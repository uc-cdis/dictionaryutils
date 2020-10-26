from dictionaryutils import dictionary


def test_no_mixed_type_in_enum():
    # An enum is said "mixed type" if the enum items don't all have the same type. The only
    # exception to this is NoneType, which is allowed in enums regardless of the type of other
    # items. This allows us to set the value to None when the property is not required
    for schema in dictionary.schema.values():
        for prop in schema["properties"].values():

            try:
                some_object_iterator = iter(prop)
            except TypeError as te:
                assert False, "{}: has non iterable property".format(schema["id"])
                # print some_object, 'is not iterable'

            if "enum" in prop:
                assert all(
                    [type(i) == str or i == None for i in prop["enum"]]
                ), "{}: enum values should all be string".format(schema["id"])


def test_lowercase_ids():
    for schema in dictionary.schema.values():
        if "id" in schema:
            assert (
                schema["id"] == schema["id"].lower()
            ), "The id in {} should be lower case".format(schema["id"])


def test_nodeid_length():
    prefix_len = len("node_")
    postfix_len = len("_node_id_idx")
    max_len = 63 - (prefix_len + postfix_len)
    for schema in dictionary.schema.values():
        if "id" in schema:
            nodeid_len = sum(map(lambda x: len(x), schema["id"].split("_")))
            assert (
                nodeid_len <= max_len
            ), "The id in {} should be at most {} characters".format(
                schema["id"], max_len
            )
