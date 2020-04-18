from library.utilities.exceptions import ApplicationException
from resource_scanner.resource_types.gcloud.instances.instances import GcloudInstancesScanner


class ResourceScanner(GcloudInstancesScanner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def scan_all_resources(self, resource_types, rules, **kwargs):
        # TODO: validate resource_types against a pre-created list
        # TODO: Break down in modular functions
        all_qualifying_resources = dict()
        for resource_type in resource_types:
            if resource_type not in all_qualifying_resources:
                all_qualifying_resources[resource_type] = list()
            scanner_function_name = f'resource_scanner__{resource_type}'
            scanner_function = getattr(self, scanner_function_name, None)
            if not scanner_function:
                raise ApplicationException(f"Unsupported resource type {resource_type}")
            self.gcloud_client.project_id = kwargs.get('project_id')
            resources_scan_data = scanner_function(**kwargs)

            for rule_id in rules:
                rule = self.rules_accessor.get_rule_by_id(rule_id=rule_id)
                filter_join_rule = rule['filter_combination']['join_rule']

                for resource_scan_data in resources_scan_data:
                    resource_id = resource_scan_data['resource_id']
                    resource_already_qualified = False

                    for qualified_resource_data in all_qualifying_resources[resource_type]:
                        if qualified_resource_data['resource_id'] == resource_id:
                            resource_already_qualified = True
                            break
                    if resource_already_qualified:
                        # REsource is already qualified due to some  other rule. Don't scan it agin
                        continue
                    rule_filter_evaluation_status = dict()

                    for rule_filter in rule['filter_criterion']:
                        # TODO: decrease local variables
                        filter_id = rule_filter['filter_id']
                        filter_type = rule_filter['filter_type']
                        filter_data = rule_filter['filter_data']
                        filter_bool = self.filter_lib.run_filter(
                            filter_type=filter_type,
                            filter_data=filter_data,
                            candidate=resource_scan_data['filter_data'][filter_type])
                        rule_filter_evaluation_status[filter_id] = filter_bool

                    resource_qualifies = self.filter_lib.summarise_all_filters_of_rule(
                        rule_filter_evaluation_status=rule_filter_evaluation_status,
                        filter_join_rule=filter_join_rule)

                    if resource_qualifies is True:
                        all_qualifying_resources[resource_type].append({'resource_id': resource_id, 'rule': rule_id})
        return all_qualifying_resources
