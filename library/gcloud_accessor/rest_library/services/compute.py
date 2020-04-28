import uuid
import time
import socket

import googleapiclient.discovery
import googleapiclient.errors

from gcloud_rest_lib_base import GcloudRestLibBase
from library.utilities.exceptions import ApplicationException
from library.utilities.logger import get_logger


# All Decorators required for this module


def compute_service_required(func):
    def new_function(*args, **kwargs):
        if args:
            self = args[0]
            if not self.compute_service:
                self.compute_service = self.initialise_compute_service_client()
        return func(*args, **kwargs)

    new_function.__name__ = func.__name__
    return new_function


def handle_delete_exceptions(func):
    def new_function(*args, **kwargs):
        self = args[0]
        try:
            result = func(*args, **kwargs)
        except googleapiclient.errors.HttpError as ex:
            if int(ex.resp['status']) == 404:
                self.logger.debug('Assuming 404 to be resource already deleted')
                result = True
            else:
                raise ex
        except ApplicationException as ex:
            if kwargs.get('suppress_exception', False):
                result = False
            else:
                raise ex
        return result

    new_function.__name__ = func.__name__
    return new_function


class GcloudCompute(GcloudRestLibBase):
    logger = get_logger('compute')
    poll_sleep_time_in_secs = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.compute_service = None

    @staticmethod
    def initialise_compute_service_client():
        return googleapiclient.discovery.build('compute', 'v1', cache_discovery=False)

    @compute_service_required
    def list_instances(self, zone):
        all_instances = self.compute_service.instances().list(project=self.project_id, zone=zone).execute()
        return all_instances

    @compute_service_required
    def list_all_instances(self):
        all_instances = self.compute_service.instances().aggregatedList(project=self.project_id).execute()
        return all_instances

    @compute_service_required
    def list_referrers_of_instance(self, zone, instance):
        return self.compute_service.instances().listReferrers(project=self.project_id, zone=zone,
                                                              instance=instance).execute()

    def list_referrers_of_all_instances(self, zone):
        return self.list_referrers_of_instance(zone=zone, instance='-')

    @compute_service_required
    def get_all_backend_services(self):
        return self.compute_service.backendServices().aggregatedList(project=self.project_id).execute()

    @compute_service_required
    def get_all_forwarding_rules(self):
        return self.compute_service.forwardingRules().aggregatedList(project=self.project_id).execute()

    @compute_service_required
    def get_all_instance_group_managers(self):
        return self.compute_service.instanceGroupManagers().aggregatedList(project=self.project_id).execute()

    @compute_service_required
    def get_all_global_url_maps(self):
        return self.compute_service.urlMaps().list(project=self.project_id).execute()

    @compute_service_required
    def get_all_regional_url_maps(self, region):
        return self.compute_service.regionUrlMaps().list(project=self.project_id, region=region).execute()

    @compute_service_required
    def get_all_global_http_proxies(self):
        return self.compute_service.targetHttpProxies().list(project=self.project_id).execute()

    @compute_service_required
    def get_all_regional_http_proxies(self, region):
        return self.compute_service.regionTargetHttpProxies().list(project=self.project_id, region=region).execute()

    @compute_service_required
    def wait_for_zonal_operation(self, zone, operation, max_timeout_mins=3):
        """
        :param region:
        :param operation:
        :param max_timeout_mins:
        :return: Bool(status), Dict(Last Operation Recieved)
        """
        # TODO: Implement max_timeout_mins
        operation_status = operation['status']
        self.logger.debug('Beginning to poll for operation')
        while operation_status != 'DONE':
            try:
                operation = self.compute_service.zoneOperations().wait(project=self.project_id, zone=zone,
                                                                       operation=operation['name']).execute()
            except socket.timeout:
                self.logger.debug('Suppressing socket timeout that occured during wait operation')
                pass
            operation_status = operation['status']
            self.logger.debug(operation)
            time.sleep(self.poll_sleep_time_in_secs)

        error = operation.get('error')
        if error:
            self.logger.exception('Error while polling for operation: {}'.format(error))
            raise ApplicationException(error)
        return operation_status == 'DONE', operation

    @compute_service_required
    def wait_for_regional_operation(self, region, operation, max_timeout_mins=3):
        """
        :param region:
        :param operation:
        :param max_timeout_mins:
        :return: Bool(status), Dict(Last Operation Recieved)
        """
        # TODO: Implement max_timeout_mins
        operation_status = operation['status']
        self.logger.debug('Beginning to poll for operation')
        while operation_status != 'DONE':
            operation = self.compute_service.regionOperations().wait(project=self.project_id, region=region,
                                                                     operation=operation['name']).execute()
            operation_status = operation['status']
            self.logger.debug(operation)
            time.sleep(self.poll_sleep_time_in_secs)

        error = operation.get('error')
        if error:
            self.logger.exception('Error while polling for operation: {}'.format(error))
            raise ApplicationException(error)
        return operation_status == 'DONE', operation

    @compute_service_required
    def wait_for_global_operation(self, operation, max_timeout_mins=3):
        """
        :param region:
        :param operation:
        :param max_timeout_mins:
        :return: Bool(status), Dict(Last Operation Recieved)
        """
        # TODO: Implement max_timeout_mins
        operation_status = operation['status']
        self.logger.debug('Beginning to poll for operation')
        while operation_status != 'DONE':
            operation = self.compute_service.globalOperations().wait(project=self.project_id,
                                                                     operation=operation['name']).execute()
            operation_status = operation['status']
            self.logger.debug(operation)
            time.sleep(self.poll_sleep_time_in_secs)

        error = operation.get('error')
        if error:
            self.logger.exception('Error while polling for operation: {}'.format(error))
            raise ApplicationException(error)
        return operation_status == 'DONE', operation

    @compute_service_required
    @handle_delete_exceptions
    def delete_forwarding_rule(self, region, forwarding_rule_name, suppress_exception=True):
        """

        :param region:
        :param forwarding_rule_name:
        :param request_id:
        :param suppress_exception: Suppresses Known Exceptions and returns false
        :return:
        """
        request_id = uuid.uuid4()
        self.logger.debug('Attempting to  delete forwarding rule {}'.format(forwarding_rule_name))

        operation = self.compute_service.forwardingRules().delete(
            project=self.project_id, region=region, forwardingRule=forwarding_rule_name, requestId=request_id
        ).execute()

        result, operation = self.wait_for_regional_operation(region=region, operation=operation)
        self.logger.debug('Delete response : {}'.format(result))
        self.logger.debug('Final operation : {}'.format(operation))
        return result

    @compute_service_required
    @handle_delete_exceptions
    def delete_global_backend_service(self, backend_service_name):
        request_id = uuid.uuid4()
        self.logger.debug('Attempting to  delete Backend Service {}'.format(backend_service_name))

        operation = self.compute_service.backendServices().delete(
            project=self.project_id, backendService=backend_service_name, requestId=request_id
        ).execute()

        result, operation = self.wait_for_global_operation(operation=operation)
        self.logger.debug('Delete response : {}'.format(result))
        self.logger.debug('Final operation : {}'.format(operation))
        return result

    @compute_service_required
    @handle_delete_exceptions
    def delete_regional_backend_service(self, region, backend_service_name):
        request_id = uuid.uuid4()
        self.logger.debug('Attempting to  delete Backend Service {}'.format(backend_service_name))

        operation = self.compute_service.regionBackendServices().delete(
            project=self.project_id, region=region, backendService=backend_service_name, requestId=request_id
        ).execute()

        result, operation = self.wait_for_regional_operation(region=region, operation=operation)
        self.logger.debug('Delete response : {}'.format(result))
        self.logger.debug('Final operation : {}'.format(operation))
        return result

    @compute_service_required
    @handle_delete_exceptions
    def delete_instance_group(self, zone, instance_group_name):
        request_id = uuid.uuid4()
        self.logger.debug('Attempting to  delete Instance Group {}'.format(instance_group_name))

        operation = self.compute_service.instanceGroups().delete(
            project=self.project_id, zone=zone, instanceGroup=instance_group_name, requestId=request_id).execute()

        result, operation = self.wait_for_zonal_operation(zone=zone, operation=operation)
        self.logger.debug('Delete response : {}'.format(result))
        self.logger.debug('Final operation : {}'.format(operation))
        return result

    @compute_service_required
    @handle_delete_exceptions
    def delete_instance(self, zone, instance_name):
        request_id = uuid.uuid4()
        self.logger.debug('Attempting to delete Instance {}'.format(instance_name))

        operation = self.compute_service.instances().delete(
            project=self.project_id, zone=zone, instance=instance_name, requestId=request_id).execute()

        result, operation = self.wait_for_zonal_operation(zone=zone, operation=operation)
        self.logger.debug('Delete response : {}'.format(result))
        self.logger.debug('Final operation : {}'.format(operation))
        return result

    @compute_service_required
    @handle_delete_exceptions
    def delete_instance_group_manager(self, zone, instance_group_manager_name):
        request_id = uuid.uuid4()
        self.logger.debug('Attempting to  delete Instance Group Manager {}'.format(instance_group_manager_name))

        operation = self.compute_service.instanceGroupManagers().delete(
            project=self.project_id, zone=zone, instanceGroupManager=instance_group_manager_name, requestId=request_id) \
            .execute()

        result, operation = self.wait_for_zonal_operation(zone=zone, operation=operation)
        self.logger.debug('Delete response : {}'.format(result))
        self.logger.debug('Final operation : {}'.format(operation))
        return result

    @compute_service_required
    @handle_delete_exceptions
    def delete_regional_url_map(self, region, url_map_name):
        request_id = uuid.uuid4()
        self.logger.debug('Attempting to  delete Regional URL Map {}'.format(url_map_name))

        operation = self.compute_service.regionUrlMaps().delete(
            project=self.project_id, region=region, urlMap=url_map_name, requestId=request_id
        ).execute()

        result, operation = self.wait_for_regional_operation(region=region, operation=operation)
        self.logger.debug('Delete response : {}'.format(result))
        self.logger.debug('Final operation : {}'.format(operation))
        return result

    @compute_service_required
    @handle_delete_exceptions
    def delete_global_url_map(self, url_map_name):
        request_id = uuid.uuid4()
        self.logger.debug('Attempting to  Global URL Map {}'.format(url_map_name))

        operation = self.compute_service.urlMaps().delete(
            project=self.project_id, urlMap=url_map_name, requestId=request_id
        ).execute()

        result, operation = self.wait_for_global_operation(operation=operation)
        self.logger.debug('Delete response : {}'.format(result))
        self.logger.debug('Final operation : {}'.format(operation))
        return result

    @compute_service_required
    @handle_delete_exceptions
    def delete_regional_http_proxy(self, http_proxy_name, region):
        request_id = uuid.uuid4()
        self.logger.debug('Attempting to  Regional HTTP Proxy {}'.format(http_proxy_name))

        operation = self.compute_service.regionTargetHttpProxies().delete(
            project=self.project_id, region=region, targetHttpProxy=http_proxy_name, requestId=request_id
        ).execute()

        result, operation = self.wait_for_global_operation(operation=operation)
        self.logger.debug('Delete response : {}'.format(result))
        self.logger.debug('Final operation : {}'.format(operation))
        return result

    @compute_service_required
    @handle_delete_exceptions
    def delete_global_http_proxy(self, http_proxy_name):
        request_id = uuid.uuid4()
        self.logger.debug('Attempting to  Global HTTP Proxy {}'.format(http_proxy_name))

        operation = self.compute_service.targetHttpProxies().delete(
            project=self.project_id, targetHttpProxy=http_proxy_name, requestId=request_id
        ).execute()

        result, operation = self.wait_for_global_operation(operation=operation)
        self.logger.debug('Delete response : {}'.format(result))
        self.logger.debug('Final operation : {}'.format(operation))
        return result


if __name__ == "__main__":
    import json

    gcloud_client = GcloudCompute()
    delete_res = gcloud_client.get_all_regional_http_proxies(region='us-central1')
    a = json.dumps(delete_res)
    print(a)
