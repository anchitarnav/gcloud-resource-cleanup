import re


def parse_link(self_link, extra_expected_values=()):
    values = dict()
    pattern = r'({}/[\w\-]+(?:/|$))'
    expected_values = ['projects', 'zones', 'regions', 'global']
    expected_values.extend(extra_expected_values)
    for identifier_value in expected_values:
        search_result = re.search(pattern=pattern.format(identifier_value), string=self_link)
        if not search_result:
            continue
        parsed_values = search_result.group().split('/')
        if len(parsed_values) < 2:
            continue
        values[identifier_value] = parsed_values[1]

    # Additional dig in
    values['api_name'] = None
    values['api_version'] = None

    values['partial_resource_type'] = None
    values['resource_name'] = None

    values['full_resource_type'] = None  # api_name.version.partial_type

    api_and_version_pattern = r'\.com/\w+/\w+'
    api_and_version_search = re.search(pattern=api_and_version_pattern, string=self_link)
    if api_and_version_search:
        parsed_values = api_and_version_search.group().split('/')
        values['api_name'] = parsed_values[1]  # Since regex is a pass two / are guaranteed
        values['api_version'] = parsed_values[2]  # Since regex is a pass two / are guaranteed

    partial_resource_name_and_type_pattern = r'[^/]+/[^/]+$'
    partial_resource_name_and_type_search = re.search(pattern=partial_resource_name_and_type_pattern, string=self_link)
    if partial_resource_name_and_type_search:
        parsed_values = partial_resource_name_and_type_search.group().split('/')
        values['partial_resource_type'] = parsed_values[0]
        values['resource_name'] = parsed_values[1]

    if values['api_name'] and values['api_version'] and values['partial_resource_type']:
        values['full_resource_type'] = f"{values['api_name']}_{values['api_version']}_{values['partial_resource_type']}"

    return values


def get_resource_type(self_link):
    return parse_link(self_link)['full_resource_type']
    # return self_link.split("/")[-2]
    # TODO: Validate against valid resource types before returning
