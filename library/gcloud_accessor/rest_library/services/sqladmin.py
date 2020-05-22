import uuid
import time
import socket

import googleapiclient.discovery
import googleapiclient.errors

from library.gcloud_accessor.rest_library.shared.gcloud_rest_lib_base import GcloudRestLibBase
from library.utilities.exceptions import ApplicationException
from library.utilities.logger import get_logger


class GcloudSqlAdmin(GcloudRestLibBase):
    logger = get_logger('compute')
    poll_sleep_time_in_secs = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sqladmin_instance = googleapiclient.discovery.build('sqladmin', 'v1beta4', cache_discovery=False)

    def list_sql_instances(self):
        return self.sqladmin_instance.instances().list(project=self.project_id).execute()


if __name__ == "__main__":
    gc = GcloudSqlAdmin()
    a = gc.list_sql_instances()
    import json

    b = json.dumps(a)
    print(b)
