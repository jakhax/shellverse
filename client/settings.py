import os 

# attackers address, you can write a method that retrieves this "sensitive "credentials in this case lets keep it simple & insecure
SERVER_ADDR="192.168.8.162"
SERVER_PORT=9999 

# FTP server credentials
FTP_SERVER_PORT=9998
FTP_SERVER_ADDR=SERVER_ADDR
FTP_USER="shellverse"
FTP_PASSWORD="read the fucking verses then bash"

RETRY_TIME=5
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  

VALID_PLATFORMS={
    "linux":"posix",
    "windows":"nt",
    "cross_platform":"all"
}

# valid plaforms: windows,linux
PLATFORM="windows"
if PLATFORM not in VALID_PLATFORMS.keys():
    raise ValueError("Invalid platform")

#LOG_FILE_PATH
LOGFILE=None

