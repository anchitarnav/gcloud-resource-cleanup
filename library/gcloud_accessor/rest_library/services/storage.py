import googleapiclient.discovery
import googleapiclient.errors

from library.gcloud_accessor.rest_library.shared.gcloud_rest_lib_base import GcloudRestLibBase
from library.utilities.logger import get_logger


class GcloudStorageV1(GcloudRestLibBase):
    logger = get_logger(__name__)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_service = googleapiclient.discovery.build('storage', 'v1', cache_discovery=False)

    def list_all_storage_buckets(self):
        return self.storage_service.buckets().list(project=self.project_id).execute()

    def list_all_objects(self, bucket_name):
        return self.storage_service.objects().list(bucket=bucket_name).execute()


if __name__ == "__main__":
    gc = GcloudStorageV1(project_id='')
    a = gc.list_all_storage_buckets()
    import json

    b = json.dumps(a)
    print(b)
