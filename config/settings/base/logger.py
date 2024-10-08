# Logging configurations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%m/%d/%Y %I:%M:%S %p'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/error.log',
            'when': 'midnight',
            'backupCount': 20,  # max file before override
            'formatter': 'standard',
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/django_request.log',
            'when': 'midnight',
            'backupCount': 20,  # max file before override
            'formatter': 'standard',
        },
    },
    'root': {
        'handlers': ['default'],
        'level': 'DEBUG',
        'propagate': True
    },
    'loggers': {
        '': {  # for default logging setup
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}