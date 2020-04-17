class GcloudInstancesScanner:
    def __init__(self, **kwargs):
        pass

    def resource_scanner__instances(self, gcloud_client, rules, **kwargs):
        """
        Filters resources that comply to the given rules
        :param gcloud_client:
        :param rule_id_list: list of rule IDs
        :return: Dict to qualifying resources in specified format
        """
        return gcloud_client.list_instances(zone='us-central1-c')
