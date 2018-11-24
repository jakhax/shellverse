from payloads.change_directory_handler import ChangeDirectoryHandler
from payloads.upload_payload_handler import FTPUploadPayloadHandler
from payloads.download_payload_handler import FTPDownloadPayloadHandler


payload_register={
    "cd":ChangeDirectoryHandler,
    "ftp-upload":FTPUploadPayloadHandler,
    "ftp-download":FTPDownloadPayloadHandler,
}