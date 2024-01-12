def gerar_arquivo_megabytes(nome_arquivo, tamanho_megabytes):
    tamanho_bytes = tamanho_megabytes * 1024 * 1024  # 1 MB = 1024 * 1024 bytes

    with open(nome_arquivo, 'wb') as arquivo:
        arquivo.write(b'\0' * tamanho_bytes)

    print(f"Arquivo '{nome_arquivo}' gerado com sucesso.")

# Exemplo de uso:
megabytes = 50
nome_do_arquivo = f'server/repository/teste{megabytes}.txt'

gerar_arquivo_megabytes(nome_do_arquivo, megabytes)