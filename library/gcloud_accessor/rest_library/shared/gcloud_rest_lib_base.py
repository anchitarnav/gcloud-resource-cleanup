from library.utilities.misc import parse_link, get_resource_type
from library.utilities.logger import get_logger
from google.auth.transport.requests import AuthorizedSession
from google.auth import default
from requests import codes

import time

from json import JSONDecodeError


class GcloudRestLibBase:
    """
    Expected to house all common functionality for Rest Client
    """
    operation_polling_time_sleep_secs = 5

    def __init__(self, project_id, **kwargs):
        # Add authentication check here
        # Add common object instantiation
        # TODO: fetch the default project from the APPLICATION CREDENTIALS JSON
        self.project_id = project_id
        self.credentials, self.default_project_id = default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
        self.session = AuthorizedSession(self.credentials)
        self.logger = get_logger(__name__)

    def wait_for_operation(self, operation, max_timeout_mins=15):
        """
        :param operation: the  operation object
        :param max_timeout_mins:
        :return: Bool(status), Dict(Last Operation Recieved)
        """
        # TODO: Implement max_timeout_mins
        operation_status = operation['status']
        self.logger.debug('Beginning to poll for operation')
        operation_self_link = operation['selfLink']
        start_time = time.time()
        while operation_status != 'DONE' and time.time() - start_time < max_timeout_mins * 60:
            self.logger.debug(f'Sleeping for {self.operation_polling_time_sleep_secs} secs before polling')
            time.sleep(self.operation_polling_time_sleep_secs)
            operation_response = self.session.post(operation_self_link + "/wait")
            if not operation_response.status_code == codes.ok:
                self.logger.error(f'Error while polling for operation {operation_response.text}')
                return False
            operation = operation_response.json()
            operation_status = operation['status']
            self.logger.debug(operation)

        error = operation.get('error')
        if error:
            self.logger.exception('Error while polling for operation: {}'.format(error))
            return False
        self.logger.debug(f"Final operation status: {operation}")
        return operation_status == 'DONE'

    def delete_self_link(self, self_link):
        del_response = self.session.delete(self_link)
        print(del_response)

        # Apprehending 404 not_found as resource already deleted
        if del_response.status_code == codes.not_found:
            self.logger.info("Apprehending 404 as resource already deleted")
            return True

        # Anything in 400 and 500 series
        del_response.raise_for_status()

        # Checking if an operation object was returned
        try:
            response_json = del_response.json()
            if "operation" in response_json.get("kind", ""):
                return self.wait_for_operation(operation=response_json)
        except ValueError:
            pass

        return True
