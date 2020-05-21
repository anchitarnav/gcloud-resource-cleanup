from library.gcloud_accessor.rest_library.services.compute import GcloudCompute
from library.gcloud_accessor.rest_library.services.sqladmin import GcloudSqlAdmin
from library.gcloud_accessor.rest_library.services.redis import GcloudRedisV1
from library.gcloud_accessor.rest_library.services.storage import GcloudStorageV1


class GcloudRestLib(GcloudCompute, GcloudSqlAdmin, GcloudRedisV1, GcloudStorageV1):
    pass
