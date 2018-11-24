import abc

class AbstractClientHandler(abc.ABC):

    @abc.abstractclassmethod
    def inject_dependencies(cls,*args, **kwargs) -> bool:
        '''
        set class attributes such as payloads register & reverse shell handler
        '''
        pass

    @abc.abstractmethod
    def __init__(self):
        '''
        set class configurations
            - server host
            - server port
        '''
        pass

    @abc.abstractmethod
    def register_signal_handler(self):
        '''
        listen for signal such as quit signal
        '''
        pass

    @abc.abstractmethod
    def quit_gracefully(self, signal=None, frame=None):
        pass

    @abc.abstractmethod
    def socket_create(self):
        '''
        create a socket instance
        '''
        pass

    @abc.abstractmethod
    def socket_connect(self):
        '''
        open scoket connection to server
        ''' 
        pass

    @abc.abstractmethod
    def send_output(self, output_str):
        '''
        send output of a command back to the server
        '''
        pass

    @abc.abstractmethod
    def receive_commands(self):
        '''
        Receive commands from remote server and run on local machine
        '''
        pass