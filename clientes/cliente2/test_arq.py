import os

def generate_large_file(file_path, size_gb):
    # 1 GB = 1024 * 1024 * 1024 bytes
    target_size = size_gb * 1024 * 1024 * 1024

    # Tamanho do bloco para escrever de uma vez (pode ajustar conforme necessário)
    block_size = 1024 * 1024  # 1 MB

    with open(file_path, 'w') as file:
        data = '0' * block_size  # Dados repetitivos
        written_size = 0

        while written_size < target_size:
            remaining_size = target_size - written_size
            current_size = min(block_size, remaining_size)
            file.write(data[:current_size])
            written_size += current_size

if __name__ == "__main__":
    file_path = "large_file.txt"
    size_gb = 0.1

    generate_large_file(file_path, size_gb)
    print(f"Arquivo '{file_path}' gerado com sucesso.")
