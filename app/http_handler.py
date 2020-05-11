import json

from flask import Flask
from library.utilities.logger import get_logger

from app.scan_rules.rules_accessor import RulesAccessor
from app.app import scan_resources, delete_scanned_resources

app = Flask(__name__)
rule_accessor = RulesAccessor()

logger = get_logger(__name__)


@app.route('/')
def index():
    logger.info("Hello.. This is a default log line .. lets see where it comes")
    return 'Hello World!'


@app.route('/scan/<project_id>/<rule_id>')
def scan(project_id, rule_id):
    if not (rule_accessor.get_rule_by_id(rule_id=rule_id, suppress_exception=True)):
        return f"Illegal rule ID. Rule ID {rule_id} not found !!", 404
    scanned_resources = scan_resources(rules=[rule_id], project_ids=[project_id])
    return f"{json.dumps(scanned_resources)}"


def scan_and_delete():
    pass
