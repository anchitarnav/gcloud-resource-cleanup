from app.resource_scanner.filter_lib import FilterLib
from library.gcloud_accessor.gcloud import Gcloud
from app.scan_rules.rules_accessor import RulesAccessor


class ResourceScannerBase:
    """
    Houses Common functions required by all scanner functions
    """

    def __init__(self, project_id, **kwargs):
        self.gcloud_client = Gcloud(project_id=project_id)
        self.filter_lib = FilterLib()
        self.rules_accessor = RulesAccessor()
