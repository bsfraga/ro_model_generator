import os
import re
import requests
from lxml import html
from concurrent.futures import ThreadPoolExecutor

URL_BASE = "https://www.spriters-resource.com/pc_computer/ragnarokonline"
DOWNLOAD_URL_TEMPLATE = "https://www.spriters-resource.com/download/{}/"

def clean_directory_name(name):
    # Remove ou substitui caracteres inválidos
    name = re.sub('[<>:"/\\|?*]', '_', name)
    return name.strip()

def fetch_and_parse_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return html.fromstring(response.content)

def extract_sprite_data(tree):
    sprite_data = []
    for element in tree.xpath("//*[@id='icon-display']/div[22]/a"):
        sprite_id = element.get("href").split("/")[-2]
        monster_name = element.xpath("./div/div[1]/span/text()")[0]
        sprite_data.append((sprite_id, monster_name))
    return sprite_data

def download_and_save_sprite(sprite_id, monster_name):
    clean_monster_name = clean_directory_name(monster_name)
    download_url = DOWNLOAD_URL_TEMPLATE.format(sprite_id)
    response = requests.get(download_url, stream=True)
    response.raise_for_status()

    # Modificar o diretório de destino para incluir "sprite_sheets"
    directory_path = os.path.join(os.getcwd(), "sprite_sheets", clean_monster_name)
    os.makedirs(directory_path, exist_ok=True)

    file_path = os.path.join(directory_path, f"{clean_monster_name}.png")
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Downloaded {monster_name}!")

def existing_directories():
    # Lista todos os diretórios dentro de "sprite_sheets"
    sprite_sheets_path = os.path.join(os.getcwd(), "sprite_sheets")
    os.makedirs(sprite_sheets_path, exist_ok=True)
    return [d for d in os.listdir(sprite_sheets_path) if os.path.isdir(os.path.join(sprite_sheets_path, d))]

def main():
    tree = fetch_and_parse_html(URL_BASE)
    sprite_data_list = extract_sprite_data(tree)

    # Obter lista de diretórios existentes
    current_dirs = existing_directories()

    # Usar ThreadPoolExecutor para baixar os sprites em paralelo
    with ThreadPoolExecutor() as executor:
        futures = []
        for sprite_id, monster_name in sprite_data_list:
            clean_monster_name = clean_directory_name(monster_name)
            if clean_monster_name not in current_dirs:
                futures.append(executor.submit(download_and_save_sprite, sprite_id, monster_name))

        # Esperar todas as tarefas concluírem e verificar se houve exceções
        for future in futures:
            future.result()

    # Print the number of directories created
    print(f"Created {len(existing_directories()) - len(current_dirs)} directories.")

if __name__ == "__main__":
    main()
