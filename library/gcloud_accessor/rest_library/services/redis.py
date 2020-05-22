import googleapiclient.discovery
import googleapiclient.errors

from library.gcloud_accessor.rest_library.shared.gcloud_rest_lib_base import GcloudRestLibBase
from library.utilities.logger import get_logger


class GcloudRedisV1(GcloudRestLibBase):
    logger = get_logger(__name__)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis_service = googleapiclient.discovery.build('redis', 'v1', cache_discovery=False)

    def list_all_redis_instances(self):
        parent = f'projects/{self.project_id}/locations/-'
        return self.redis_service.projects().locations().instances().list(parent=parent).execute()


if __name__ == "__main__":
    gc = GcloudRedisV1(project_id='')
    a = gc.list_all_redis_instances()
    import json

    b = json.dumps(a)
    print(b)
