import os
import yaml

from pathlib import Path

from library.utilities.exceptions import ApplicationException
from library.utilities.logger import get_logger


class RulesAccessor:
    logger = get_logger(__name__)
    one_time_folder = os.path.join(str(Path(os.path.realpath(__file__)).parent), 'rules')

    def __init__(self):
        self.all_rules = dict()
        self.read_all_rules()

    def read_all_rules(self):
        # Possible reading from DB in future.
        # Reading from filesystem for now
        self.logger.debug('Reading Rules ..')
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
            raise ApplicationException(f"Rule {rule_id} not Found !!")
        return rule
