import abc
class AbstractPayloadHandler(abc.ABC):
    @abc.abstractmethod
    def execute_payload(self,data:bytes) -> str:
        pass
