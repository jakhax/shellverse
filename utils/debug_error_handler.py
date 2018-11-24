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