from logger import get_logger
from library.gcloud_accessor.gcloud import Gcloud
from library.utilities.misc import parse_link, get_resource_type


class ResourceDeletionHandler:
    def __init__(self):
        self.logger = get_logger(__file__.replace('py', ''))
        self.gcloud_lib = Gcloud()

    def delete_stack(self, iterable):
        """
        :param iterable: an iterable with self_link as strings
        :return: bool
        """
        if not iterable:
            return

        stack_deletion_status = None
        resource_deletion_status = []
        for resource_id in iterable:
            self.logger.info(f'Initialising resource deletion for resource ID {resource_id}')

            # Check if resource types is supported in code yet
            resource_type = get_resource_type(resource_id)
            deletion_function_name = f'delete__{resource_type}'
            deletion_function = getattr(self, deletion_function_name, None)
            if not deletion_function:
                self.logger.info(f'Could not figure out how to delete resource of type : {resource_type}')
                self.logger.warning('Aborting deletion of entire stack ..')
                break

            # Initiate deletion
            delete_result = deletion_function(resource_id)
            resource_deletion_status.append(delete_result)

            if not delete_result:
                self.logger.error(f'Deletion failed for resource {resource_id}')
                self.logger.error('Aborting entire stack as it can have dependencies')
                break
            else:
                self.logger.info(f'Deletion Successful for resource ID: {resource_id}')

        if False in resource_deletion_status:
            stack_deletion_status = False

        return bool(stack_deletion_status)

    def delete__instances(self, resource_id):
        self_link_values = parse_link(self_link=resource_id, extra_expected_values=['instances'])
        delete_res = self.gcloud_lib.delete_instance(
            zone=self_link_values['zones'], instance_name=self_link_values['instances'])
        return delete_res

    def delete__instanceGroups(self, resource_id):
        self_link_values = parse_link(self_link=resource_id, extra_expected_values=['instanceGroups'])
        delete_res = self.gcloud_lib.delete_instance_group(
            zone=self_link_values['zones'], instance_group_name=self_link_values['instanceGroups'])
        return delete_res

    def delete__instanceGroupManagers(self, resource_id):
        self_link_values = parse_link(self_link=resource_id, extra_expected_values=['instanceGroupManagers'])
        delete_res = self.gcloud_lib.delete_instance_group_manager(
            zone=self_link_values['zones'], instance_group_manager_name=self_link_values['instanceGroupManagers'])
        return delete_res

    def delete__backendServices(self, resource_id):
        self_link_values = parse_link(self_link=resource_id, extra_expected_values=['backendServices'])
        if 'regions' in self_link_values:
            delete_res = self.gcloud_lib.delete_regional_backend_service(
                region=self_link_values['regions'], backend_service_name=self_link_values['backendServices'])
        elif 'global' in self_link_values:
            delete_res = self.gcloud_lib.delete_global_backend_service(
                backend_service_name=self_link_values['backendServices'])
        else:
            self.logger.warning('Could not figure out how to delete backendService : {}'.format(resource_id))
            delete_res = False
        return delete_res

    def delete__forwardingRules(self, resource_id):
        self_link_values = parse_link(self_link=resource_id, extra_expected_values=['forwardingRules'])
        delete_res = self.gcloud_lib.delete_forwarding_rule(region=self_link_values['regions'],
                                                            forwarding_rule_name=self_link_values['forwardingRules'])
        return delete_res
