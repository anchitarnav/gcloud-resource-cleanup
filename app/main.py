from resource_scanner.resource_scanner import ResourceScanner
from dependency_resolver.dependency_resolver import DependencyResolver
from deletion_handler.resource_deletion import ResourceDeletionHandler

# Temp Import
import secrets
import sys

# Temp Queue. Later adapt to cloud based queue
all_scanned_resources = dict()

# 1. Scan resources
resource_scanner = ResourceScanner()
deletion_handler = ResourceDeletionHandler()

# TODO: Filter which rules to run and on what resource types
rules_to_run = ['R_ABC_00004']

for project_id in secrets.all_project_ids:
    scanned_resources = resource_scanner.scan_all_resources(resource_types=['instances'], rules=rules_to_run,
                                                            project_id=project_id)
    all_scanned_resources[project_id] = scanned_resources

print(all_scanned_resources)
sys.exit(0)

dependency_resolver = DependencyResolver()

for project_id, project_data in all_scanned_resources.items():
    for scanned_resource_type, scanned_resources in project_data.items():
        for resource in scanned_resources:
            dependency_stack = dependency_resolver.resolve_dependencies(
                resource_id=resource['resource_id'], resource_type=scanned_resource_type)
            print(dependency_stack)
            dependency_stack.reverse()
            # res = deletion_handler.delete_stack(dependency_stack)
            # print(res)

# 2. Delete resources
# delete_resources(all_scanned_resources)

# TODO: To be implemented

# ref = gcloud_client.list_referrers_of_all_instances(zone=zone)
# print(json.dumps(ref))
