import socket
import os
import threading
import time

def is_file_in_directory(file_name, directory_path='repository'):
    # ... (mesmo que seu código original)

def send_command(client_socket, command, *params):
    # ... (mesmo que seu código original)

def receive_response(client_socket):
    # ... (mesmo que seu código original)

def upload_file(client_socket, file_name):
    if is_file_in_directory(file_name):
        send_command(client_socket, 'upload', file_name)

        file_path = os.path.join('repository', file_name)
        file_size = os.path.getsize(file_path)

        start_time = time.time()
        start_byte_count = 0

        transfer_rates = []
        elapsed_times = []

        with open(file_path, 'rb') as file:
            while True:
                file_content = file.read(1024)
                if not file_content:
                    break

                client_socket.send(file_content)
                end_byte_count = file.tell()

                elapsed_time = time.time() - start_time
                elapsed_time_in_seconds = int(elapsed_time)
                if elapsed_time_in_seconds > 0 and end_byte_count > start_byte_count:
                    transfer_rate = (end_byte_count - start_byte_count) / elapsed_time_in_seconds  # em bytes por segundo
                    transfer_rates.append(transfer_rate)
                    elapsed_times.append(elapsed_time)

                start_byte_count = end_byte_count

        client_socket.send('$$enviado$$'.encode('utf-8'))
        end_time = time.time()
        elapsed_time = end_time - start_time
        transfer_rate = file_size / elapsed_time  # em bytes por segundo
        print(f'Arquivo enviado em {elapsed_time:.2f} segundos. Taxa de transferência média: {transfer_rate:.2f} bytes por segundo')

        return transfer_rates, elapsed_times

    else:
        print('Arquivo não encontrado. Ele deve estar na pasta repository.')
        return [], []

def download_file(client_socket, file_name, dest_path='repository'):
    # ... (mesmo que seu código original)

def client_thread():
    # ... (mesmo que seu código original)

if __name__ == '__main__':
    # ... (mesmo que seu código original)
