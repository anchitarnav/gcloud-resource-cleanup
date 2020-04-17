class GcloudRestLibBase:
    """
    Expected to house all common functionality for Rest Client
    """

    def __init__(self, **kwargs):
        # Add authentication check here
        # Add common object instantiation
        # TODO: fetch the default project from the APPLICATION CREDENTIALS JSON
        self.project_id = kwargs.get('project_id', 'durable-trainer-251010')
