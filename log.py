import logging.config
DISPLAY_LOG = 'DEBUG'
logger = logging.getLogger(__name__)


try:
    fh = open('info.log','r')
    fh.close()
except:
    fh = open('info.log','w')
    fh.close()


try:
    fh = open('errors.log','r')
    fh.close()
except:
    fh = open('errors.log','w')
    fh.close()

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "info.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            },

            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": "errors.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            }
        },

        "loggers": {
            "my_module": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": "no"
            }
        },

        "root": {
            "level": DISPLAY_LOG,
            "handlers": ["console", "info_file_handler", "error_file_handler"]
        }
    }
)
logger.info('*********************************************')
logger.info('*********************************************')
logger.info('*******Starting GIGA DE TESTE IRRICONTROL*******')
logger.info('*********************************************')
logger.info('*********************************************')
