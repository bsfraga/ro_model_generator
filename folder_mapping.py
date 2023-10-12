import os

def list_files(startpath, output_file):
    for root, dirs, files in os.walk(startpath):
        # Calcula o nível do diretório atual para ajustar a indentação
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        
        # Escreve o nome do diretório atual no arquivo de saída com a indentação
        output_file.write(f"{indent}[{os.path.basename(root)}]\n")
        
        # Indentação para os arquivos
        subindent = '│   ' * level
        
        # Escreve os arquivos deste diretório no arquivo de saída
        for i, f in enumerate(files):
            # Se for o último arquivo, usa "└──" em vez de "├──"
            file_indent = '└── ' if i == len(files) - 1 else '├── '
            output_file.write(f"{subindent}{file_indent}{f}\n")

# Chama a função começando pelo diretório do script e escreve no arquivo
if __name__ == "__main__":
    output_filename = "output_structure.txt"
    with open(output_filename, 'w', encoding='utf-8') as f:
        list_files(os.path.dirname(os.path.realpath(__file__)), f)
    print(f"Estrutura de diretórios e arquivos escrita em {output_filename}")
