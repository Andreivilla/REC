import socket
import os
from threading import Thread
import time

def is_file_in_directory(file_name, directory_path='repository'):
    # Constrói o caminho completo do arquivo
    file_path = os.path.join(directory_path, file_name)
    # Verifica se o arquivo existe no caminho especificado
    return os.path.isfile(file_path)

def list_files():
    files = os.listdir('repository')
    return '\n'.join(files)

def upload_file(client_socket, file_name):
    print('recebendo arquivo')
    try:
        with open('repository/'+file_name, 'wb') as file:
            while True:
                file_content = client_socket.recv(1024)
                
                if b'$$enviado$$' in  file_content:
                    file_content = file_content.replace(b'$$enviado$$', b"")
                    file.write(file_content)
                    break
                
                file.write(file_content)
        print('arquivo recebido')
                
    except Exception as e:
        print(f"Erro ao receber o arquivo {file_name}: {e}")

def download_file(client_socket, file_name):
    if is_file_in_directory(file_name):
        with open(f'repository/{file_name}', 'rb') as file:
            
            #tentativa de contar time
            start_time = time.time()
            total_bytes_send = 0
            
            file_content = file.read(1024)
            while file_content:
                client_socket.send(file_content)

                total_bytes_send += len(file_content)

                file_content = file.read(1024)       
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            transfer_rate = total_bytes_send/elapsed_time / 1024 #kilobytes por segundo
            print(f'Taxa de transferência: {transfer_rate:.2f} KB/s')

        #return file_content
        client_socket.send('$$enviado$$'.encode('utf-8'))
        print('arquivo enviado')
    else:
        client_socket.send('$$file not found$$'.encode('utf-8'))
        

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
            upload_file(client_socket, file_name)
            continue
        elif command == 'download':
            file_name, path= params
            download_file(client_socket, file_name)
            continue 
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
