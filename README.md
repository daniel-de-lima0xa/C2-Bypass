# Socket Server Interaction

This project consists of a socket server implemented in Python for interacting with remote clients. It supports connections on two different ports and allows clients to send encrypted PowerShell commands to be executed on the server.

## Features

- **Remote Connection**: Connect to remote servers by specifying an IP address and port.
- **PowerShell Command Execution**: Execute PowerShell commands on the remote server.
- **Background Session Management**: Maintain sessions in the background for later resumption.
- **Active Session Listing**: List sessions in the background, including information such as IP address and port.
- **Connection Termination**: Terminate the connection with the server remotely.
- **Interaction with Background Sessions**: Choose a background session to interact with.
- **Listening for Connections from Any Source**: Listen for connections from any source on a local server.

## Usage

To use this server, simply execute the Python script `socket_server.py`. Make sure you have Python installed on your system.

## Demonstration


![EDR](https://github.com/daniel-de-lima0xa/TelegramBotHub/assets/59209081/0c4044de-f03b-465e-8a04-84e5c97a10e1)


```bash
python socket_server.py

python socket_implante.py




