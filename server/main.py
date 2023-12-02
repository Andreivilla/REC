import socket
import threading
import os

def receive_file(client_socket, file_name):
    try:
        with open(file_name, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
    except Exception as e:
        print(f"Erro ao receber o arquivo {file_name}: {e}")
    finally:
        client_socket.close()

def handle_client(client_socket, addr):
    print(f"Conexão recebida de {addr}")

    file_name = client_socket.recv(1024).decode()
    print(f"Recebendo arquivo: {file_name}")

    receive_file(client_socket, file_name)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '127.0.0.1'
    server_port = 8888

    server_socket.bind((server_host, server_port))
    server_socket.listen(5)

    print(f"Servidor escutando em {server_host}:{server_port}")

    while True:
        client_socket, addr = server_socket.accept()

        # Use uma nova thread para lidar com a conexão do cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
