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


class Scanner__Redis_V1_Instances(ResourceScannerBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def resource_scanner__redis_v1_instances(self, **kwargs):
        """
        Filters resources that comply to the given rules
        :param gcloud_client:
        :param rule_id_list: list of rule IDs
        :return: Dict to qualifying resources in specified format
        """
        to_return = list()
        all_instances = self.gcloud_client.list_all_redis_instances()

        for instance in all_instances.get('instances', []):
            instance_name = instance['name'].split('/')[-1]
            # Name Expected Format: projects/{projectId}/locations/{locationId}/instances/{instanceId}

            instance_age = int(time.time() - iso8601.parse_date(instance['createTime']).timestamp())
            instance_tags = instance.get('labels', {})
            instance_self_link = f"https://redis.googleapis.com/v1/{instance['name']}"

            instance_literals = [
                literal
                for possible_literals in (instance_tags.keys(), instance_tags.values(), [instance_name])
                for literal in possible_literals if literal
            ]

            temp_dict = {
                "resource_id": instance_self_link,
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
