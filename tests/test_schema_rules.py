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
    # prepended to node id: (https://github.com/uc-cdis/psqlgraph/blob/3.0.0/psqlgraph/base.py#L14)
    prefix_len = len("node_")
    # postpended to node id: (https://github.com/uc-cdis/psqlgraph/blob/3.0.0/psqlgraph/node.py#L121)
    postfix_len = len("_node_id_idx")
    # maximum identifier allowed in postgres is 63 characters:
    max_len = 63 - (prefix_len + postfix_len)
    for schema in dictionary.schema.values():
        if "id" in schema:
            # (https://github.com/uc-cdis/gdcdatamodel/blob/daa709e1a71e0b8985f306c0a6bffe439ee18be7/gdcdatamodel/models/__init__.py#L161)
            nodeid_len = len(schema["id"].replace("_", ""))
            assert (
                nodeid_len <= max_len
            ), "The id in {} should be at most {} characters (not counting underscores)".format(
                schema["id"], max_len
            )
