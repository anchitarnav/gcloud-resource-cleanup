import iso8601
import time

from resource_scanner.resource_types.resource_scanner_base import ResourceScannerBase

return_format = [
    {
        "resource_id": "selfLink",
        "filter_data": {
            'NAME': ""  # This can be anything .. even a dict
        }
    }
]


class GcloudInstancesScanner(ResourceScannerBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def resource_scanner__instances(self, **kwargs):
        """
        Filters resources that comply to the given rules
        :param gcloud_client:
        :param rule_id_list: list of rule IDs
        :return: Dict to qualifying resources in specified format
        """
        to_return = list()
        all_instances_response = self.gcloud_client.list_all_instances()
        all_instances = []
        for zone_name in all_instances_response['items']:
            if 'instances' in all_instances_response['items'][zone_name]:
                all_instances.extend(all_instances_response['items'][zone_name]['instances'])

        for instance in all_instances:
            temp_dict = {
                "resource_id": instance['selfLink'],
                "filter_data": {
                    "NAME": instance['name'],
                    "AGE": int(time.time() - iso8601.parse_date(instance['creationTimestamp']).timestamp())
                    # Age of instance in seconds
                }
            }

            # Additional modifications can be done here
            to_return.append(temp_dict)
        return to_return
