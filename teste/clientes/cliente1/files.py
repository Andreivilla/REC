import os
from datetime import datetime
def add_file(name, date):
    file_path = 'data/files.txt'
    with open(file_path, 'a') as file:
        file.write(f"{name}, {date}\n")
def del_file(name):
    file_path = 'data/files.txt'
    temp_file_path = 'data/temp_files.txt'
    with open(file_path, 'r') as file, open(temp_file_path, 'w') as temp_file:
        lines = file.readlines()
        for line in lines:
            if name not in line:
                temp_file.write(line)
    os.remove(file_path)
    os.rename(temp_file_path, file_path)
def list_files():
    file_path = 'data/files.txt'
    result = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            name, date = map(str.strip, line.split(','))
            result.append((name, date))
    return result
def receive_file(client_socket, file_name):
    try:
        with open('data/' + file_name, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
    except Exception as e:
        print(f"Erro ao receber o arquivo {file_name}: {e}")
    finally:
        client_socket.close()
# Example Usage:
#current_date = datetime.now().strftime("%Y-%m-%d")
#add_file("File1", current_date)
#add_file("File2", current_date)
#print("Before Deletion:")
#print(ler_files())
#del_file("File1")
#print("\nAfter Deletion:")
#print(ler_files())