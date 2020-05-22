import argparse

from app.app import scan_resources, delete_scanned_resources
from library.utilities.logger import get_logger

logger = get_logger(__name__)

parser = argparse.ArgumentParser(description="GCP resource Scan and deletion framework")
parser.add_argument("action",
                    choices=['scan', 'delete'],
                    metavar="action",
                    type=str,
                    nargs='?',
                    default='scan',
                    help='The action that you perform using the rule. scan or delete')

parser.add_argument('--project_id',
                    nargs="+",
                    required=True,
                    help='Your GCP project ID which you want to scan')

parser.add_argument('--rules',
                    nargs="+",
                    metavar='RULE_ID',
                    default=['a_week_old_resources'],
                    help='the rule IDs that you want to run')

arguments = parser.parse_args()

print(f'\n\nReceived request to {arguments.action} for rules {arguments.rules} on project IDs: {arguments.project_id}')
print(f'\nInitiating resource {arguments.action} ..')

scanned_resources = scan_resources(rules=arguments.rules, project_ids=arguments.project_id)
logger.info(f'Resource scan info : {scanned_resources}')

FLAG_DELETE_RESOURCES = False
if arguments.action == 'delete':
    print("\n\n"
          "Do you want to delete the above resources and all it's dependencies ?? ..\n"
          "Only 'yes' shall be taken as a valid option.\n\n"
          "This is not reversible and causes permanent deletion", end="..: ")
    FLAG_DELETE_RESOURCES = input().strip().lower() == "yes"

if FLAG_DELETE_RESOURCES:
    logger.info(f'Deleting resources ..')
    # delete_scanned_resources(all_scanned_resources=scanned_resources)
