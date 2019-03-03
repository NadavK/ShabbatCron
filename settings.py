import logging.config

ASTRAL_LOCATION_INFO = """Raanana,Israel,32°11'N,34°52'E,Asia/Jerusalem,48
    TelAviv,Israel,32°4'N,34°47'E,Asia/Jerusalem,5"""
LOCATION = 'Raanana'

START_DELTA = 30  # how many minutes after Shabbat to run the START_SCRIPT
END_DELTA = -30   # how many minutes after Motzei to run the END_SCRIPT
START_SCRIPT = 'start.sh'
END_SCRIPT = 'end.sh'

try:
    # A good practice is to keep all the secret data in a separate file
    from settings_secret import *
except:
    pass


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s]\t[%(name)s] %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'ShabbatCron.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 50,
            'formatter': 'standard',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'root': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}

logging.config.dictConfig(LOGGING)
