import os
import json
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from collections import defaultdict

def process_json_file(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    if not data:  # Verificando se os dados estão vazios
        return

    # Agrupa as imagens por dimensão
    dimension_groups = defaultdict(list)
    for item in data:
        key = (item["width"], item["height"])
        dimension_groups[key].append(item)

    # Descobre o grupo com a maior quantidade de imagens
    largest_group_key = max(dimension_groups, key=lambda k: len(dimension_groups[k]), default=None)

    # Se não houver um grupo maior, retorne
    if not largest_group_key:
        return

    largest_group = dimension_groups[largest_group_key]
    # Calcula a cor dominante média para o maior grupo
    mean_dominant_color = np.mean([np.array(item["dominant_color"]) for item in largest_group], axis=0)

    # Filtra as imagens que estão próximas da cor dominante média
    color_tolerance = 0.1
    filtered_data = [
        item for item in data
        if all(mean_dominant_color[i] - color_tolerance * mean_dominant_color[i] <= item["dominant_color"][i] <= mean_dominant_color[i] + color_tolerance * mean_dominant_color[i] for i in range(3))
    ]
    
    # Sobrescrever o arquivo JSON com os dados filtrados
    with open(json_path, 'w') as f:
        json.dump(filtered_data, f, indent=4)

    # remover os arquivos de imagem que não estão na lista de dados filtrados
    directory = os.path.dirname(json_path)
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            sprite_id = filename.split(".")[0]
            if not any(item["id"] == sprite_id for item in filtered_data):
                os.remove(os.path.join(directory, filename))


def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_path = os.path.join(directory, filename)
            try:
                process_json_file(json_path)
            except Exception as e:
                print(f"Erro ao processar {json_path}. Erro: {e}")

def main():
    base_dir = 'training_data'
    if not os.path.exists(base_dir):
        print(f"O diretório {base_dir} não foi encontrado.")
        return
    
    subdirectories = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    with ProcessPoolExecutor(max_workers=12) as executor:
        executor.map(process_directory, subdirectories)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script interrompido pelo usuário.")
