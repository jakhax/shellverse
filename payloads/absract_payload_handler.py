import abc
class AbstractPayloadHandler(abc.ABC):

    @abc.abstractclassmethod
    def get_platform(cls):
        return ""

    @abc.abstractmethod
    def execute_payload(self,data:bytes) -> str:
        pass
