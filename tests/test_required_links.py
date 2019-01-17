from dictionaryutils import dictionary


def test_require_core_metadata_collections():
    for schema in dictionary.schema.values():
        if schema["category"].endswith("_file"):
            assert (
                "core_metadata_collections" in schema["properties"]
            ), "core_metadata_collections is required for data node {}".format(
                schema["id"]
            )


def test_required_fields_in_links():
    for schema in dictionary.schema.values():
        for link in schema["links"]:
            if not "subgroup" in link:
                for nodeprops in schema["properties"][link["name"]]["anyOf"][0][
                    "items"
                ]["properties"]:
                    assert (
                        nodeprops
                        in dictionary.schema[link["target_type"]]["properties"]
                    ), "Link {} requires a property {} that doesn't exist in target type {}".format(
                        link["name"], nodeprops, link["target_type"]
                    )
