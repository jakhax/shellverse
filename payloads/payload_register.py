from payloads.change_directory_handler import ChangeDirectoryHandler
from payloads.upload_payload_handler import FTPUploadPayloadHandler


payload_register={
    "cd":ChangeDirectoryHandler,
    "upload":FTPUploadPayloadHandler,
}