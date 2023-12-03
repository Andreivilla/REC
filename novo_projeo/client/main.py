import socket

def send_command(client_socket, command, *params):
    data = ' '.join([command, *params])
    client_socket.sendall(data.encode('utf-8'))

def receive_response(client_socket):
    return client_socket.recv(1024).decode('utf-8')

def upload_file(client_socket, file_name):
    with open(file_name, 'rb') as file:
        file_content = file.read()
    send_command(client_socket, 'upload', file_name)
    client_socket.sendall(file_content)
    response = receive_response(client_socket)
    print(response)

def download_file(client_socket, file_name, dest_path):
    send_command(client_socket, 'download', file_name, dest_path)
    #file_content = client_socket.recv(1024)
    try:
        with open(dest_path + '/' + file_name, 'wb') as file:
            while True:
                file_content = client_socket.recv(1024)
                if file_content == b'$$enviado$$':
                    break
                file.write(file_content)
        print('arquivo recebido')
                
    except Exception as e:
        print(f"Erro ao receber o arquivo {file_name}: {e}")
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))

    while True:
        user_input = input('Enter command: ')
        #command, *params = 'download a.txt repository'.split()#user_input.split()
        command, *params = user_input.split()

        if command == 'exit':
            send_command(client_socket, 'exit')
            break
        elif command == 'list':#ok funfa
            send_command(client_socket, 'list')
        elif command == 'upload':
            file_name, = params
            upload_file(client_socket, file_name)
            continue
        elif command == 'download':#ok funfa
            file_name, dest_path = params
            download_file(client_socket, file_name, dest_path)
            continue
        elif command == 'delete':
            file_name, = params
            send_command(client_socket, 'delete', file_name)
        else:
            print('Invalid command.')
            continue

        response = receive_response(client_socket)
        print(response)

    client_socket.close()

if __name__ == '__main__':
    main()
