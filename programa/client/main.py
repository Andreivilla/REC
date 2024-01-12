import socket
import os
def is_file_in_directory(file_name, directory_path='repository'):
    # Constrói o caminho completo do arquivo
    file_path = os.path.join(directory_path, file_name)
    # Verifica se o arquivo existe no caminho especificado
    return os.path.isfile(file_path)

def send_command(client_socket, command, *params):
    data = ' '.join([command, *params])
    client_socket.sendall(data.encode('utf-8'))

def receive_response(client_socket):
    return client_socket.recv(1024).decode('utf-8')

def upload_file(client_socket, file_name):
    if is_file_in_directory(file_name):
        send_command(client_socket, 'upload', file_name)

        with open(f'repository/{file_name}', 'rb') as file:
            file_content = file.read(1024)
            while file_content:
                client_socket.send(file_content)
                file_content = file.read(1024)
        #return file_content
        client_socket.send('$$enviado$$'.encode('utf-8'))
        print('arquivo enviado')
    else:
        print('Arquivo não encontrado ele deve estar na pasta repository')
        return

def download_file(client_socket, file_name, dest_path=None):
    if dest_path == None:
        dest_path = 'repository'
    else:
        try:
            os.mkdir('repository/' + dest_path)#se não houver diretorio ele cria
            dest_path = 'repository/' + dest_path
        except Exception as e:
            dest_path = 'repository/' + dest_path
    
    send_command(client_socket, 'download', file_name, dest_path)
    #file_content = client_socket.recv(1024)
    try:
        with open(dest_path + '/' + file_name, 'wb') as file:
            while True:
                file_content = client_socket.recv(1024)
                #recebe resposta que o servidor não achou o arquivo
                if file_content == b'$$file not found$$':
                    os.remove(dest_path + '/' + file_name)
                    print('arquivo não encontrado')
                    return
                
                if b'$$enviado$$' in  file_content:
                    file_content = file_content.replace(b'$$enviado$$', b"")
                    file.write(file_content)
                    break

                print(f'baixando arquivo') 
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
        #upload d.txt

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
            if len(params)> 1:
                file_name, dest_path = params
                download_file(client_socket, file_name, dest_path)
            else:
                file_name, = params
                download_file(client_socket, file_name)
            continue
        elif command == 'delete':
            file_name, = params
            send_command(client_socket, 'delete', file_name)
        else:
            print('Invalid command.')
            continue
        
        #input('impit')

        response = receive_response(client_socket)
        print(response)

    client_socket.close()

if __name__ == '__main__':
    main()
