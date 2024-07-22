import os

import colorlog
from decouple import config

from helpers.files import ensure_directory_exists

ACTIVE_LOGGER_APPS = config('ACTIVE_LOGGER_APPS', cast=lambda v: [
    s.strip() for s in v.split(',')])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

log_dir = os.path.join(BASE_DIR, 'logs')
ensure_directory_exists(log_dir)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'style': '%',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
            'style': '%',
        },
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(reset)s%(message)s',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
    },
    'handlers': {
        'file': {
            'level': config('LOG_LEVEL_FILE'),
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_dir, 'log.txt'),
            'formatter': 'verbose',
        },
        'console': {
            'level': config('LOG_LEVEL_CONSOLE'),
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
    },
    'loggers': {
        **{
            logger_name: {
                'handlers': ['file', 'console'],
                'level': 'DEBUG',
                'propagate': True,
            } for logger_name in ACTIVE_LOGGER_APPS
        },
    }
}
