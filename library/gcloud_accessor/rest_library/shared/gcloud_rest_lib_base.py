# TODO: Remove secrets import.
import secrets

from library.utilities.misc import parse_link, get_resource_type

class GcloudRestLibBase:
    """
    Expected to house all common functionality for Rest Client
    """

    def __init__(self, **kwargs):
        # Add authentication check here
        # Add common object instantiation
        # TODO: fetch the default project from the APPLICATION CREDENTIALS JSON
        self.project_id = kwargs.get('project_id', secrets.project_1)
