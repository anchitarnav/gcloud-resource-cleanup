import iso8601
import time

from app.resource_scanner.resource_types.resource_scanner_base import ResourceScannerBase

return_format = [
    {
        "resource_id": "selfLink",
        "filter_data": {
            'NAME': ""  # This can be anything .. even a dict
        }
    }
]


class Scanner__Sql_V1beta4_Instances(ResourceScannerBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def resource_scanner__sql_v1beta4_instances(self, **kwargs):
        """
        Filters resources that comply to the given rules
        :param gcloud_client:
        :param rule_id_list: list of rule IDs
        :return: Dict to qualifying resources in specified format
        """
        to_return = list()
        all_instances = self.gcloud_client.list_sql_instances()

        for instance in all_instances.get('items', []):
            instance_name = instance['name']

            # Hack: Using creation time of the serverCaCert as the creation time of the instance as well
            # In future if this fails, go to the operations API and find time of CREATE  event
            # https://cloud.google.com/sql/docs/mysql/admin-api/rest/v1beta4/operations/list
            instance_age = int(time.time() - iso8601.parse_date(instance['serverCaCert']['createTime']).timestamp())
            instance_tags = instance['settings'].get('userLabels', {})
            instance_literals = [
                literal
                for possible_literals in (instance_tags.keys(), instance_tags.values(), [instance_name])
                for literal in possible_literals if literal
            ]

            temp_dict = {
                "resource_id": instance['selfLink'],
                "filter_data": {
                    # Instance Name
                    "NAME": instance_name,

                    # Age of instance in seconds
                    "AGE": instance_age,

                    # Dict: Key: value for all labels on instance. Value can be "" as well
                    'TAG': instance_tags,

                    # All literals, including the name, keys, values
                    'AUTODETECT_DECLARED_EXPIRY': {'literals': instance_literals, 'age': instance_age}
                }
            }
            # Additional modifications can be done here
            to_return.append(temp_dict)
        return to_return
