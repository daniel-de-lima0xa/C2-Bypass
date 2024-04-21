# Socket Server Interaction

Este projeto consiste em um servidor socket implementado em Python para interação com clientes remotos. Ele oferece suporte a conexões em duas portas diferentes e permite que os clientes enviem comandos PowerShell criptografados para serem executados no servidor.

## Funcionalidades

- **Conexão Remota**: Conectar-se a servidores remotos especificando um endereço IP e porta.
- **Execução de Comandos PowerShell**: Executar comandos PowerShell no servidor remoto.
- **Gerenciamento de Sessões em Segundo Plano**: Deixar sessões em segundo plano para retomá-las posteriormente.
- **Listagem de Sessões Ativas**: Listar sessões em segundo plano, incluindo informações como endereço IP e porta.
- **Encerramento de Conexão**: Encerrar a conexão com o servidor remotamente.
- **Interagir com Sessões em Segundo Plano**: Escolher uma sessão em segundo plano para interagir.
- **Escuta de Conexões de Qualquer Origem**: Escutar conexões de qualquer origem em um servidor local.

## Uso

Para utilizar este servidor, basta executar o script Python `socket_server.py`. Certifique-se de ter o Python instalado em seu sistema.

## Demonstração

![EDR](https://github.com/daniel-de-lima0xa/TelegramBotHub/assets/59209081/0c4044de-f03b-465e-8a04-84e5c97a10e1)


```bash
python socket_server.py

python socket_implante.py




