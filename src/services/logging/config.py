import os

LOGGING_CONFIG_FILENAME = "api_logging_config.json"
ROTATION_CONDITITON = '100MB'
LOGS_FILENAME = os.environ.get('LOGS_FILENAME')
