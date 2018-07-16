from dictionaryutils import dictionary


def test_required_nodes():
    required_nodes = [
        'program', 'project'
    ]
    for node in required_nodes:
        assert node in dictionary.schema, \
            '{} is a required node but not in the dictionary'.format(node)

def test_required_data_fields():
    required_fields = [
        'data_type', 'data_format', 'data_category', 'object_id'
    ]
    for schema in dictionary.schema.values():
        if schema['category'].endswith('_file'):
            for field in required_fields:
                assert field in schema['properties'], \
                    '{} is required but not in {}'.format(field, schema['id'])

def test_required_project_fields():
    required_fields = [
        'availability_type', 'code', 'dbgap_accession_number', 'id', 'type'
    ]
    schema = dictionary.schema['project']
    for field in required_fields:
        assert field in schema['properties'], \
            '{} is required for project'.format(field)

def test_required_program_fields():
    required_fields = [
        'id', 'type'
    ]
    schema = dictionary.schema['program']
    for field in required_fields:
        assert field in schema['properties'], \
            '{} is required for program'.format(field)

def test_required_ubiquitous_fields():
    required_fields = [
        'updated_datetime', 'created_datetime', 'id', 'type'
    ]
    for schema in dictionary.schema.values():
        if not schema['id'] == 'program' and not schema['id'] == 'project' \
            and not schema['id'] == 'root':
            for field in required_fields:
                assert field in schema['properties'], \
                    '{} is required but not in {}'.format(field, schema['id'])

def test_id_matches():
    # file names must match id files...
    for key, schema in dictionary.schema.items():
        assert key == schema['id'], \
            '{} file has unmatched id {}'.format(key, schema['id'])

