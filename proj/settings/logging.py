import os
from pathlib import Path
from pythonjsonlogger import jsonlogger
import logging

LOG_BASE_DIR = Path(__file__).resolve().parent.parent.parent

class APILogFormatter(logging.Formatter):
    """
        custom formatter for API log
        adds method, path and ip to log if available
    """
    def format(self, record):
        record.method = getattr(record, 'method', '')
        record.path = getattr(record, 'path', '')
        record.ip = getattr(record, 'ip', '')
        record.status_code = getattr(record, 'status_code', '')

        return super().format(record)

class APILogJsonFormatter(jsonlogger.JsonFormatter):
    def format(self, record):
        record.method = getattr(record, 'method', '')
        record.path = getattr(record, 'path', '')
        record.ip = getattr(record, 'ip', '')
        record.status_code = getattr(record, 'status_code', '')

        return super().format(record)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'api': {
            '()': APILogFormatter,
            'format': '{levelname} {asctime} {method} {path} {status_code} {ip} {message}',
            'style': '{',
        },
        'json': {
            '()': APILogJsonFormatter, 
            'format': '%(levelname)s %(asctime)s %(method)s %(path)s %(status_code)s  %(ip)s %(message)s',
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'api_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
        'api_v1_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.environ.get('API_LOG_FILE', os.path.join(LOG_BASE_DIR, 'logs/api_v1.log')),
            'maxBytes': 1024 * 1024 * 20,  # 20 MB
            'backupCount': 10,
            'formatter': 'json',
        },
    },
    'loggers': {
        # General Logger for all Django related logs
        'django': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        # logger for APIs version 1
        'v1': {
            'handlers': ['api_console', 'api_v1_file' ],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
