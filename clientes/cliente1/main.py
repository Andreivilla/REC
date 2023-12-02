import socket

def send_file(file_name):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_host = '127.0.0.1'
        server_port = 8888

        client_socket.connect((server_host, server_port))

        # Enviar nome do arquivo
        client_socket.send(file_name.encode())

        # Enviar o arquivo em partes
        with open(file_name, 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)

        print(f"Arquivo {file_name} enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar o arquivo: {e}")
    finally:
        client_socket.close()

def main():
    file_to_send = 'test_file_1.txt'
    send_file(file_to_send)

if __name__ == "__main__":
    main()
