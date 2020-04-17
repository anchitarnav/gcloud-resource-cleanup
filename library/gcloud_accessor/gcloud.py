import googleapiclient.discovery

from library.gcloud_accessor.rest_library.gcloud_rest_library import GcloudRestLib


class Gcloud(GcloudRestLib):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
