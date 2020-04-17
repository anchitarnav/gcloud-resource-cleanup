from library.utilities.exceptions import ApplicationException
from library.gcloud_accessor.gcloud import Gcloud
from resource_scanner.resource_types.gcloud.instances.instances import GcloudInstancesScanner


class ResourceScanner(GcloudInstancesScanner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gcloud_client = Gcloud()

    def scan_all_resources(self, resource_types, rules, **kwargs):
        # TODO: validate resource_types against a pre-created list
        for resource_type in resource_types:
            scanner_function_name = f'resource_scanner__{resource_type}'
            scanner_function = getattr(self, scanner_function_name, None)
            if not scanner_function:
                raise ApplicationException(f"Unsupported resource type {resource_type}")
            self.gcloud_client.project_id = kwargs.get('project_id')
            return scanner_function(gcloud_client=self.gcloud_client, rules=rules, **kwargs)
