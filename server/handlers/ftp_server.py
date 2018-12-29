import logging
from server import settings
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler

def pyftpdlib_logging():
    date_format = "%Y/%m/%d %H:%M:%S"
    log_file_path = settings.FTP_LOGFILE
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    # own_module_logger = logging.getLogger(__name__)
    pyftpdlib_logger = logging.getLogger("pyftpdlib")
    # Setup logging to file (Only pyftpdlib)
    filehandler = logging.FileHandler(filename = log_file_path)
    filehandler.setLevel(logging.DEBUG)
    fileformatter = logging.Formatter(fmt = "%(asctime)s - %(levelname)-8s - %(name)s.%(funcName)s - %(message)s",
                                    datefmt = date_format)
    filehandler.setFormatter(fileformatter)
    pyftpdlib_logger.addHandler(filehandler)
    pyftpdlib_logger.propagate = False

def basic_ftp_server():
    authorizer = DummyAuthorizer()
    # read https://pyftpdlib.readthedocs.io/en/latest/api.html permissions section
    authorizer.add_user(settings.FTP_USER, settings.FTP_PASSWORD, homedir=settings.FTP_DIR, perm='elrafmwMT')
    if settings.FTP_OVER_TLS:
        # Requires PyOpenSSL module (http://pypi.python.org/pypi/pyOpenSSL).
        from pyftpdlib.handlers import TLS_FTPHandler
        handler = TLS_FTPHandler
        handler.certfile = settings.FTP_TLS_CERT
        handler.authorizer = authorizer
        # requires SSL for both control and data channel
        #handler.tls_control_required = True
        #handler.tls_data_required = True
    else:
        handler = FTPHandler
        handler.authorizer = authorizer
    pyftpdlib_logging()
    # logging.basicConfig(filename=settings.FTP_LOGFILE, level=logging.DEBUG)
    server = FTPServer((settings.FTP_SERVER_ADDR, settings.FTP_SERVER_PORT), handler)
    server.serve_forever()








