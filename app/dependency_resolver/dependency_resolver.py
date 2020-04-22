import re
from library.gcloud_accessor.gcloud import Gcloud


class DependencyResolver:
    def __init__(self):
        self.gcloud_lib = Gcloud()

    def resolve_dependencies(self, resource_type, resource_id):
        resolver_function = getattr(self, f'dependency_resolver__{resource_type}')
        return resolver_function(resource_id=resource_id)

    def parse_link(self, self_link):
        values = dict()
        pattern = r'({}/[\w\-]+(?:/|$))'
        expected_values = ['projects', 'zones', 'instances']
        for identifier_value in expected_values:
            search_result = re.search(pattern=pattern.format(identifier_value), string=self_link)
            if not search_result:
                continue
            parsed_values = search_result.group().split('/')
            if len(parsed_values) < 2:
                continue
            values[identifier_value] = parsed_values[1]
        return values

    def get_resource_type(self, self_link):
        return self_link.split("/")[-2]
        # TODO: Validate against valid resource types before returning
        # If gke in result, its a kubernetes cluster

    def dependency_resolver__instances(self, resource_id):
        #  The stack to return at end
        dependency_stack = [resource_id]

        instance_self_link = resource_id
        self_link_values = self.parse_link(self_link=instance_self_link)
        # TODO: Handle case when self_link parsing fails. Raise Customer exception

        zone = self_link_values.get('zones')
        instance_name = self_link_values.get('instances')

        # Get list of resources referring to this instance (dependencies)
        instance_referrers = self.gcloud_lib.list_referrers_of_instance(zone=zone, instance=instance_name)

        # If there are no dependencies, the instance is idependent
        if 'items' not in instance_referrers:
            return dependency_stack

        # If there are dependencies:
        for referrer_details in instance_referrers['items']:
            # TODO: Handle if resource type could not be guessed
            # 1. Get the dependency type
            referrer_resource_type = self.get_resource_type(self_link=referrer_details['referrer'])

            # 2. Dynamic Determine Call the function that handles this type of resource
            function_to_resolve = getattr(self, f'dependency_resolver__{referrer_resource_type}', None)
            if not function_to_resolve:
                print(f'Dont know how to resolve referrer of type {referrer_resource_type}')
                continue
            referrer_stack = function_to_resolve(referrer_details['referrer'])

            # 3. If the function returns its own stack, push to existing stack
            if referrer_stack:
                dependency_stack.extend(referrer_stack)

        return dependency_stack

    def dependency_resolver__instanceGroups(self, resource_id):
        """
        :param resource_id: Expected to be selfLink of an instanceGroup
        :return: List of dependent resources. List containing self if no dependents
        """
        to_return_stack = [resource_id]

        # Since we don't have a direct API that can give instance groups
        # We shall have to check all possible places where an InstanceGroup Can be referred

        # 1. Backend Services
        all_backend_services_info = self.gcloud_lib.get_all_backend_services()

        # There are no backend services in the entire project
        if 'items' not in all_backend_services_info:
            return to_return_stack

        # Looping over resources in each region
        for region, region_info in all_backend_services_info['items'].items():  # region -> can be 'global' as well

            # There are no backend services in this region
            if 'backendServices' not in region_info:
                continue

            # Looping over every backend service in a region
            for backend_service_info in region_info['backendServices']:

                # Not concerned about external load balancers here
                if not ('loadBalancingScheme' in backend_service_info and 'INTERNAL' in backend_service_info[
                    'loadBalancingScheme']):
                    continue

                if 'backends' not in backend_service_info:
                    continue

                for backend_info in backend_service_info['backends']:

                    # This backend actually refers to the required instanceGroup
                    if 'group' in backend_info and backend_info['group'] == resource_id:
                        referrer_resource_id = backend_service_info['selfLink']

                        # Get resource type. Expected: backendService
                        referrer_resource_type = self.get_resource_type(self_link=referrer_resource_id)

                        # Check if we have a function that can further resolve dependencies
                        function_to_resolve = getattr(self, f'dependency_resolver__{referrer_resource_type}', None)
                        if not function_to_resolve:
                            print(f'Dont know how to resolve referrer of type {referrer_resource_type}')
                            # At least add to stack what we have discovered
                            to_return_stack.append(referrer_resource_id)
                            continue

                        # Call the corresponding function to resolve further dependecies
                        referrer_stack = function_to_resolve(referrer_resource_id)

                        if referrer_stack:
                            to_return_stack.extend(referrer_stack)
                        break
        return to_return_stack

    def dependency_resolver__backendServices(self, resource_id):
        """
        Check for resources that refer this backendService and return them
        :param resource_id: Expected to be selfLink od BackendService
        :return: List
        """
        to_return_stack = [resource_id]

        # 1. Checking Forwarding Rules where this backend service is listed
        # 1a. Get info of all backend services

        all_forwarding_rules = self.gcloud_lib.get_all_forwarding_rules()

        if 'items' not in all_forwarding_rules:
            return to_return_stack

        for region, region_forwarding_rules_info in all_forwarding_rules['items'].items():

            # There are no forwarding rules in this region
            if 'forwardingRules' not in region_forwarding_rules_info:
                continue

            for forwarding_rule in region_forwarding_rules_info['forwardingRules']:
                if 'backendService' in forwarding_rule and forwarding_rule['backendService'] == resource_id:
                    to_return_stack.append(forwarding_rule['selfLink'])

        return to_return_stack


if __name__ == "__main__":
    dependency_resolver = DependencyResolver()
    dependency_resolver.resolve_dependencies(resource_type='instances', resource_id='')
