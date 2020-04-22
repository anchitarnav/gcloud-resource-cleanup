from logger import get_logger
from library.gcloud_accessor.gcloud import Gcloud
from library.utilities.misc import parse_link, get_resource_type


class ResourceDeletionHandler:
    def __init__(self):
        self.logger = get_logger(__file__.replace('py', ''))
        self.gcloud_lib = Gcloud()

    def delete_stack(self, iterable):
        """
        Expecting iterable to be an iterable with self_link as strings
        :param iterable:
        :return:
        """
        for resource_id in iterable:
            resource_type = get_resource_type(resource_id)
            deletion_function_name = f'delete__{resource_type}'
            deletion_function = getattr(self, deletion_function_name, None)
            if not deletion_function:
                self.logger.info(f'Could not figure out how to delete resource of type : {resource_type}')
                self.logger.warning('Aborting deletion of entire stack ..')
                break
            delete_result = deletion_function(resource_id)

    def delete__forwardingRules(self, resource_id):
        self_link_values = parse_link(self_link=resource_id)
        delete_res = self.gcloud_lib.delete_forwarding_rule(region=self_link_values['regions'],
                                                            forwarding_rule=self_link_values['forwardingRules'])
        return delete_res
