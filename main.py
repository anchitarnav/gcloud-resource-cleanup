from app.app import scan_resources, delete_scanned_resources
from app.http_handler import app

from library.utilities.logger import get_logger

logger = get_logger(__name__)

# Local run
if __name__ == '__main__':
    RUN_AS_FLASK_APP = True

    if RUN_AS_FLASK_APP:
        app.run(host='127.0.0.1', port=8080, debug=True)
    else:
        import secrets

        rules_to_run = ['R_ABC_00003']
        project_ids = secrets.all_project_ids
        logger.info(f'Recieved request to scan project IDs: {project_ids} for rules {rules_to_run}')

        logger.info('Initiating resource scan ..')
        scanned_resources = scan_resources(rules=rules_to_run, project_ids=project_ids)
        logger.info(f'Resource scan info : {scanned_resources}')

        FLAG_DELETE_RESOURCES = True

        if FLAG_DELETE_RESOURCES:
            delete_scanned_resources(all_scanned_resources=scanned_resources)
