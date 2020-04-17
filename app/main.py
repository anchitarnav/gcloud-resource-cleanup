from resource_scanner.resource_scanner import ResourceScanner

# Temp Queue. Later adapt to cloud based queue
all_scanned_resources = []

# 1. Scan resources
resource_scanner = ResourceScanner()

# TODO: Filter which rules to run
rules_to_run = ['R_ABC_00001']

all_project_ids = ['durable-trainer-251010']
for project_id in all_project_ids:
    scanned_resources = resource_scanner.scan_all_resources(resource_types=['instances'], rules=rules_to_run,
                                                            project_id=project_id)
    all_scanned_resources.append(scanned_resources)

print(all_scanned_resources)

# 2. Delete resources
# delete_resources(all_scanned_resources)

# TODO: To be implemented

# ref = gcloud_client.list_referrers_of_all_instances(zone=zone)
# print(json.dumps(ref))
