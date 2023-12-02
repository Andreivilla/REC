import socket
import threading
from files import *
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

#def missing_files_send(file_list):


def handle_client(client_socket, addr):
    print(f"Conexão recebida de {addr}")

    #cliente se conecta e o servidor envia a lsita de arquivos
    files_list = str(list_files())
    client_socket.sendall(files_list.encode())
    
    #envia lista e espera resposta
    response = client_socket.recv(1024).decode()
    if response != 'OK':#se não for ok é pq falta arquivos precisam ser enviados
        missing_files = extrair_info_string(response)
        for file in missing_files:#envia tds os arquivos faltantes
            file_name = file[0]
            #file_date = str(missing_files[i][1])
            # Enviar nome do arquivo
            #print(file_name)
            try:
                print(f'enviando arquivo {file_name}')
                client_socket.send(str(file_name).encode())
                #client_socket.send(file_date.encode())
                #Enviar o arquivo em partes
                with open('data/'+file_name, 'rb') as file:
                    data = file.read(1024)
                    
                    while data:
                        client_socket.send(data)
                        data = file.read(1024)
                        if not data:
                            break
                print('seeafawf')
                confirmacao = client_socket.recv(1024).decode()
                print('fawfawfawf')
                print(confirmacao)
                print(f"Arquivo {file_name} enviado com sucesso!")                    
            except Exception as e:
                print(f"Erro ao enviar o arquivo: {e}")
            finally:
                client_socket.close()

    #file_name = client_socket.recv(1024).decode()
    #print(f"Recebendo arquivo: {file_name}")

    #receive_file(client_socket, file_name)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '127.0.0.1'
    server_port = 8888

    server_socket.bind((server_host, server_port))
    server_socket.listen(5)#limite de clietes na fila não ativos

    print(f"Servidor escutando em {server_host}:{server_port}")

    while True:
        client_socket, addr = server_socket.accept()

        # Use uma nova thread para lidar com a conexão do cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
