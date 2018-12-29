import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  

#  address to listen on
SERVER_ADDR="127.0.0.1"
SERVER_PORT=9999 

# FTP server credentials
FTP_SERVER_ADDR=SERVER_ADDR
FTP_SERVER_PORT=9998
FTP_USER="shellverse"
FTP_PASSWORD="read the fucking verses then bash"
FTP_LOGFILE=os.path.expanduser("~/ftp_shellverse.log")
FTP_DIR=os.path.expanduser("~/shellverse_ftp")
if not os.path.exists(FTP_DIR or os.path.isdir(FTP_DIR)):
    os.mkdir(os.path.expanduser("~/shellverse_ftp"))

# TLS support
FTP_OVER_TLS=False
FTP_TLS_CERT=None

#LOG_FILE_PATH
LOGFILE=os.path.expanduser("~/shellverse.log")

# retry time for creating server socket
RETRY_TIME=5

