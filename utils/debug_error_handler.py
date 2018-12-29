import os
from typing import Tuple

class ErrorLogHandler:

    def __init__(self,*args, **kwargs):
        pass
    def logError(self,sys_exec_info:Tuple,e,toPrint:bool=False):
        self.error=e
        self.exc_type, self.exc_obj, self.exc_tb = sys_exec_info
        self.fname = os.path.split(self.exc_tb.tb_frame.f_code.co_filename)[1]
        self.error_message="{} {} {}\n {}".format(self.exc_type,self.fname,self.exc_tb.tb_lineno,self.error)
        # log error
        if toPrint:
            print(self.error_message)



import os
import logging.config


class LogHandler:
    def get_logger(self,name,log_file_path=None,*args, **kwargs):
        if log_file_path is None:
            log_file_path=os.path.expanduser("~/sonic.log")
        config_default = {
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
                    "level": "INFO",
                    "formatter": "simple",
                    "stream": "ext://sys.stdout"
                },
                "error_file_handler": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "INFO",
                    "formatter": "simple",
                    "filename": log_file_path,
                    "maxBytes": 10485760,
                    "backupCount": 20,
                    "encoding": "utf8"
                },
            },
            "root": {
                "level": "DEBUG",
                "handlers": ["console", "error_file_handler"]
            }
        }
        logging.config.dictConfig(config_default)
        return logging.getLogger(name)