import os
import yaml


class RulesAccessor:
    one_time_folder = 'scan_rules/one-time'

    def __init__(self):
        self.all_rules = dict()
        self.read_all_rules()

    def read_all_rules(self):
        # Possible reading from DB in future.
        # Reading from filesystem for now
        for yaml_file in os.listdir(self.one_time_folder):
            with open(os.path.join(self.one_time_folder, yaml_file)) as fp:
                y_contents = yaml.load(fp, Loader=yaml.BaseLoader)
                self.all_rules[y_contents['rule_id']] = y_contents

        # self.all_yaml_files.extend(os.listdir('scan_rules/persistent'))

    def get_rule_by_id(self, rule_id):
        return self.all_rules.get(rule_id)
