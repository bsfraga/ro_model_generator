import os

def crawler():
    total_files = 0
    extensions_count = {}
    empty_dirs = []

    root_dir = os.getcwd()

    for subdir, _, files in os.walk(root_dir):
        if subdir == root_dir:
            continue

        if not files:
            empty_dirs.append(subdir)
            continue

        for file in files:
            _, ext = os.path.splitext(file)
            if ext:
                ext = ext[1:]
            extensions_count[ext] = extensions_count.get(ext, 0) + 1
            total_files += 1

    return total_files, extensions_count, empty_dirs

def main():
    try:
        total_files, extensions_count, empty_dirs = crawler()

        print(f"Nome do diretório: {os.path.basename(os.getcwd())}")
        print(f"Quantidade total de arquivos: {total_files}")
        for ext, count in extensions_count.items():
            print(f"- {ext if ext else 'Sem extensão'}: {count}")
        
        print(f"\nNúmero de diretórios vazios: {len(empty_dirs)}")
        for d in empty_dirs:
            print(d)

    except Exception as e:
        print(f"Erro ao executar o script: {e}")

if __name__ == "__main__":
    main()
