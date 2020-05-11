from app.resource_scanner.resource_scanner import ResourceScanner
from app.dependency_resolver.dependency_resolver import DependencyResolver
from app.deletion_handler.resource_deletion import ResourceDeletionHandler

from library.utilities.logger import get_logger

logger = get_logger(__name__)


def delete_scanned_resources(all_scanned_resources):
    dependency_resolver = DependencyResolver()
    deletion_handler = ResourceDeletionHandler()

    for project_id, project_data in all_scanned_resources.items():
        for scanned_resource_type, scanned_resources in project_data.items():
            for resource in scanned_resources:
                logger.debug(f'Beginning resource deletion for {resource}')
                logger.debug('Initiating dependency scanner')
                dependency_stack = dependency_resolver.resolve_dependencies(
                    resource_id=resource['resource_id'], resource_type=scanned_resource_type)
                logger.debug(f"Dependency stack => {dependency_stack}")
                dependency_stack.reverse()
                res = deletion_handler.delete_stack(dependency_stack)
                print(res)


def scan_resources(rules, project_ids):
    resource_scanner = ResourceScanner()
    all_scanned_resources = dict()

    for project_id in project_ids:
        scanned_resources_for_proj = resource_scanner.scan_all_resources(resource_types=['instances'], rules=rules,
                                                                         project_id=project_id)
        all_scanned_resources[project_id] = scanned_resources_for_proj
    return all_scanned_resources
