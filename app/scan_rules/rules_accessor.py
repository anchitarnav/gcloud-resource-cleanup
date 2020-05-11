import os
import yaml

from google.cloud import storage
from pathlib import Path

from library.utilities.exceptions import ApplicationException
from library.utilities.logger import get_logger

RULES_BUCKET_NAME = os.environ.get('RULES_BUCKET_NAME')


class RulesAccessor:
    one_time_folder = os.path.join(str(Path(os.path.realpath(__file__)).parent), 'one-time')
    logger = get_logger(__name__)

    def __init__(self):
        self.all_rules = dict()
        if RULES_BUCKET_NAME:
            self.read_rules_from_gcs_bucket(bucket_name=RULES_BUCKET_NAME)
        else:
            self.read_all_rules()

    def read_rules_from_gcs_bucket(self, bucket_name):
        self.logger.info(f'Trying to read rules from  {bucket_name}')
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)

        all_blobs = bucket.list_blobs()
        all_blob_names = [blob.name for blob in all_blobs]
        self.logger.info(f"Rule Files Present: {all_blob_names}")

        for blob_name in all_blob_names:
            blob = bucket.get_blob(blob_name)
            blob_string = blob.download_as_string()
            y_contents = yaml.safe_load(blob_string)
            self.all_rules[y_contents['rule_id']] = y_contents

        self.logger.info(f'Read the following rule IDs: {self.all_rules.keys()}')

    def read_all_rules(self):
        # Possible reading from DB in future.
        # Reading from filesystem for now
        for yaml_file in os.listdir(self.one_time_folder):
            with open(os.path.join(self.one_time_folder, yaml_file)) as fp:
                y_contents = yaml.load(fp, Loader=yaml.BaseLoader)
                self.all_rules[y_contents['rule_id']] = y_contents

        # self.all_yaml_files.extend(os.listdir('scan_rules/persistent'))

    def get_rule_by_id(self, rule_id, suppress_exception=False):
        rule = self.all_rules.get(rule_id)
        if not suppress_exception and not rule:
            self.logger.error(f'Rule {rule_id} not Found !')
            self.logger.error(f"Valid rules are {list(self.all_rules.keys())}")
            raise ApplicationException("Rule not Found !!")
        return rule
