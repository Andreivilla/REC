from datetime import datetime

class File_Manager:
    def __init__(self, file_path='file_list.txt'):
        self.file_list_path = file_path
        self.file_list = self.read_or_create_file_list()

    def read_or_create_file_list(self):
        file_list = []
        try:
            with open(self.file_list_path, 'r') as file:
                for line in file:
                    file_info = line.strip().split(', ')
                    if len(file_info) == 2:
                        file_list.append({'nome': file_info[0], 'data': file_info[1]})
        except FileNotFoundError:
            print(f"O arquivo '{self.file_list_path}' não foi encontrado. Criando o arquivo...")
            open(self.file_list_path, 'w')#cria arquivo
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")

        return file_list
    
    def file_exists(self, file_name):
        # Verifica se um arquivo está na lista
        return any(entry['nome'] == file_name for entry in self.file_list)

    def update_file(self):
        # Atualiza o arquivo 'file_list.txt' com base em self.file_list
        with open(self.file_list_path, 'w') as file:
            #file.write("# Exemplo de formato:\n# nome_do_arquivo, data\n")
            for entry in self.file_list:
                file.write(f"{entry['nome']}, {entry['data']}\n")

    def add_file(self, file_name):
        if self.file_exists(file_name):
            self.delete_file(file_name)#se já tiver o arquivo apaga ele
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_entry = {'nome': file_name, 'data': current_datetime}
        self.file_list.append(new_entry)
        self.update_file()

    #lsit
    def list_file(self):
        return self.file_list
    #download    
    # #upload
    def upload_file(self, file):  
        self.add_file(file)
    #delete
    def delete_file(self, file_name):
        # Exclui um arquivo da lista e atualiza o arquivo
        self.file_list = [entry for entry in self.file_list if entry['nome'] != file_name]
        self.update_file()
    


    
fm = File_Manager()
fm.add_file('teste.txt')
#fm.delete_file('teste.txt')