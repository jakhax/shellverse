
import os
import sys
from payloads.absract_payload_handler import AbstractPayloadHandler
from utils.debug_error_handler import ErrorLogHandler

error_logger= ErrorLogHandler()

class WindowsWallchangePayloadHandler(AbstractPayloadHandler):
    def execute_payload(self, data):
        
        try:
            import win32api, win32con, win32gui
            data=data.decode("utf-8")
            paths=data.split()[1]
            key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
            win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
            win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
            win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1+2)
            return "Command execution successful\n"
        except Exception as e:
            error_logger.logError(sys.exc_info(), e, True)
            return "Command execution unsuccessful: {}\n".format(str(e))



    
