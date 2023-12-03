import socket
import os
from threading import Thread

def list_files():
    files = os.listdir('repository')
    return '\n'.join(files)

def upload_file(client_soket, file_name):
    with open('repository/'+file_name, wb) as file



    #with open(f'repository/{file_name}', 'wb') as file:
    #    file.write(file_content)
    #return f'{file_name} uploaded successfully.'

def download_file(client_socket, file_name):
    try:
        with open(f'repository/{file_name}', 'rb') as file:
            file_content = file.read(1024)
            while file_content:
                client_socket.send(file_content)
                file_content = file.read(1024)
        #return file_content
        client_socket.send('$$enviado$$'.encode('utf-8'))
        print('arquivo enviado')
    except FileNotFoundError:
        return f'File {file_name} not found.'

def delete_file(file_name):
    try:
        os.remove(f'repository/{file_name}')
        return f'{file_name} deleted successfully.'
    except FileNotFoundError:
        return f'File {file_name} not found.'

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        command, *params = data.split()

        if command == 'list':
            response = list_files()
            
        elif command == 'upload':
            file_name, = params
            #file_content = client_socket.recv(1024)
            #response = upload_file(file_content, file_name)
            upload_file(client_socket, file_name)
            continue
        elif command == 'download':
            file_name, dest_path = params
            file_content = download_file(client_socket, file_name)
            #client_socket.sendall(file_content)
            continue  # Skip response message after sending file content
        elif command == 'delete':
            file_name, = params
            response = delete_file(file_name)
        elif command == 'exit':
            response = 'Server shutting down.'
            break
        else:
            response = 'Invalid command.'

        client_socket.sendall(response.encode('utf-8'))

    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8888))
    server_socket.listen(5)

    print('Server listening on port 8888...')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Accepted connection from {addr}')
        client_handler = Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    if not os.path.exists('repository'):
        os.makedirs('repository')
    start_server()
