import re


class FilterLib:
    def run_filter(self, filter_type, filter_data, candidate):
        # TODO: evaluate the filter based on filter type and then return boolean
        filter_function_name = f'filter_handler__{filter_type.lower()}'
        filter_function = getattr(self, filter_function_name, None)
        # TODO: Handle illegal filter case
        return filter_function(filter_data, candidate)

    def summarise_all_filters_of_rule(self, rule_filter_evaluation_status, filter_join_rule):
        for filter_id, filter_status in rule_filter_evaluation_status.items():
            filter_join_rule = filter_join_rule.replace(filter_id, str(filter_status))
        return bool(eval(filter_join_rule))

    # TODO: Put all filter handlers together
    def filter_handler__name(self, filter_data, candidate):
        name_regex = filter_data['name_regex']
        # In  the present case the candidate is a  string.
        # TODO: Document this contract centrally
        return bool(re.search(pattern=name_regex, string=candidate))

    def filter_handler__age(self, filter_data, candidate):
        """
        Presently the candidate is an int -> Age  of resource  in seconds
        :param filter_data:
        :param candidate:
        :return: bool
        """
        multiplier_to_secs = {'days': 24 * 60 * 60, 'hours': 60 * 60}
        amount = int(filter_data['age'])
        unit = filter_data['unit']
        return bool(candidate - amount * multiplier_to_secs[unit] > 0)

    def filter_handler__tag(self, filter_data, candidate):
        """
        :param filter_data:
        :param candidate: Expected: Dict of key value pairs. Accepts blank dict as well
        :return: bool
        """
        expected_key_regex = filter_data['key']
        expected_value_regex = filter_data.get('value', None)

        for actual_label_key, actual_label_value in candidate.items():
            if not re.search(pattern=expected_key_regex, string=actual_label_key):
                continue

            # Key is passing. Yet to check if a value should pass as well
            if not expected_value_regex:
                # No value check specified.
                # Every rule can check for just 1 tag. So done with checking
                return True

            if re.search(pattern=expected_value_regex, string=actual_label_value):
                return True

        return False
