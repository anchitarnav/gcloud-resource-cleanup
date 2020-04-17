import googleapiclient.discovery

from gcloud_rest_lib_base import GcloudRestLibBase


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


class GcloudCompute(GcloudRestLibBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.compute_service = None

    @staticmethod
    def initialise_compute_service_client():
        return googleapiclient.discovery.build('compute', 'v1')

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
