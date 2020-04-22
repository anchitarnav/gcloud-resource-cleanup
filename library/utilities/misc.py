import re


def parse_link(self_link, extra_expected_values=()):
    values = dict()
    pattern = r'({}/[\w\-]+(?:/|$))'
    expected_values = ['projects', 'zones', 'instances', 'regions', 'forwardingRules']
    expected_values.extend(extra_expected_values)
    for identifier_value in expected_values:
        search_result = re.search(pattern=pattern.format(identifier_value), string=self_link)
        if not search_result:
            continue
        parsed_values = search_result.group().split('/')
        if len(parsed_values) < 2:
            continue
        values[identifier_value] = parsed_values[1]
    return values


def get_resource_type(self_link):
    return self_link.split("/")[-2]
    # TODO: Validate against valid resource types before returning
    # If gke in result, its a kubernetes cluster
