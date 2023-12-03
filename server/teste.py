import os

def is_file_in_directory(file_name, directory_path='repository'):
    # Constrói o caminho completo do arquivo
    file_path = os.path.join(directory_path, file_name)

    # Verifica se o arquivo existe no caminho especificado
    return os.path.isfile(file_path)

# Exemplo de uso
file_name_to_check = 'asnghjk.txt'
if is_file_in_directory(file_name_to_check):
    print(f'O arquivo {file_name_to_check} está no diretório.')
else:
    print(f'O arquivo {file_name_to_check} não está no diretório.')
