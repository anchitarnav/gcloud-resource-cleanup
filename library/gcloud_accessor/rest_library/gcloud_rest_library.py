from library.gcloud_accessor.rest_library.services.compute import GcloudCompute
from library.gcloud_accessor.rest_library.services.sqladmin import GcloudSqlAdmin


class GcloudRestLib(GcloudCompute, GcloudSqlAdmin):
    pass
