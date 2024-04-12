# Este projeto consiste em um programa Python para interagir com servidores remotos usando sockets.

## Funcionalidades

- Conexão a servidores remotos especificando endereço IP e porta.
- Envio de comandos PowerShell para o servidor remoto.
- Gerenciamento de sessões em segundo plano.
- Listagem de sessões em segundo plano, incluindo informações como endereço IP e porta.
- Encerramento da conexão com o servidor remoto.
- Escolha de uma sessão em segundo plano para interagir.
- Escuta de conexões de qualquer origem em um servidor local.

## Uso

Para utilizar este programa, basta clonar o repositório e executar o script Python `socket_client.py`. Certifique-se de ter o Python instalado em seu sistema.

```bash
python socket_client.py


Socket Server Interaction
Este projeto consiste em um servidor socket implementado em Python para interação com clientes remotos. Ele oferece suporte a conexões em duas portas diferentes e permite que os clientes enviem comandos PowerShell criptografados para serem executados no servidor.

Funcionalidades
Conexão a servidores remotos especificando endereço IP e porta.
Envio de comandos PowerShell criptografados para o servidor remoto.
Gerenciamento de sessões em segundo plano.
Listagem de sessões em segundo plano, incluindo informações como endereço IP e porta.
Encerramento da conexão com o servidor remoto.
Escuta de conexões de qualquer origem em um servidor local.
Implementação
O servidor foi implementado utilizando a biblioteca padrão socket do Python para comunicação em rede e threading para lidar com múltiplas conexões simultaneamente. A criptografia XOR é aplicada aos dados transmitidos entre o cliente e o servidor para garantir a segurança das informações.

Uso
Para utilizar este servidor, basta executar o script Python socket_server.py. Certifique-se de ter o Python instalado em seu sistema.

bash
Copy code
python socket_server.py
