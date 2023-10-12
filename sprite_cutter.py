import cv2
import json
import os
import uuid
import subprocess
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import time
import shutil
import numpy as np

def get_dominant_color(image, k=1, resize_dim=(64, 64)):
    """
    Retorna a cor dominante da imagem usando o algoritmo k-means.
    """
    # Redimensionando a imagem para otimizar a velocidade de processamento
    image = cv2.resize(image, resize_dim, interpolation=cv2.INTER_AREA)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convertendo para RGB
    pixels = image.reshape((-1, 3))
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.2)
    _, labels, palette = cv2.kmeans(pixels.astype(np.float32), k, None, criteria, 3, cv2.KMEANS_RANDOM_CENTERS)
    _, counts = np.unique(labels, return_counts=True)
    
    # Retorna a cor do cluster dominante
    return palette[np.argmax(counts)].tolist()

def fix_png_images(directory):
    subprocess.run(["magick", "mogrify", "*.png"], cwd=directory)

def is_valid_sprite(sprite, threshold_non_white=0.90, color_std_threshold=10):
    # Convertendo a imagem para espaço de cores HSV (para lidar melhor com variações de iluminação)
    hsv = cv2.cvtColor(sprite, cv2.COLOR_BGR2HSV)
    
    # Criando uma máscara para pixels não brancos
    # Consideramos um pixel não totalmente branco se ele não estiver muito próximo do branco
    # Aqui, estamos considerando qualquer pixel com valor (em HSV) abaixo de 245 como não branco
    non_white_mask = cv2.inRange(hsv, (0, 0, 0), (255, 255, 245))

    # Contando pixels não brancos
    non_white_count = cv2.countNonZero(non_white_mask)

    # Calculando a proporção de pixels não brancos
    total_pixels = sprite.shape[0] * sprite.shape[1]
    ratio_non_white = non_white_count / total_pixels

    # Calculando o desvio padrão dos canais de cor
    color_std = sprite.std(axis=(0, 1))

    # Verificando a variação de cores (verificando se o desvio padrão em qualquer canal de cor é maior que um limiar)
    has_color_variation = any(std_val > color_std_threshold for std_val in color_std)

    # Verificando se ambos os critérios são atendidos
    return ratio_non_white > threshold_non_white and has_color_variation

def extract_sprite_coordinates_from_sheet(image_path, output_dir):
    if not os.path.exists(image_path):
        return []
    
    try:
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            print(f"Erro ao ler a imagem: {image_path}")
            return []

        sprite_coordinates = []

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Pré-processamento: Aplica um desfoque gaussiano para reduzir o ruído
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        # Ajusta os limiares do Canny
        canny_output = cv2.Canny(blurred_image, 50, 150)

        contours, _ = cv2.findContours(canny_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Pós-processamento: Considera apenas contornos de tamanho significativo
            if cv2.contourArea(contour) > 200:
                x, y, w, h = cv2.boundingRect(contour)
                sprite_image = image[y:y+h, x:x+w]  # Mova esta linha para cima
                sprite_id = str(uuid.uuid4())
                dominant_color = get_dominant_color(sprite_image)

                sprite_coordinates.append({
                    'id': sprite_id,
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h,
                    'dominant_color': dominant_color
                })

                sprite_filename = os.path.join(output_dir, f"{sprite_id}.png")
                cv2.imwrite(sprite_filename, sprite_image, [cv2.IMWRITE_PNG_COMPRESSION, 9])

                fix_png_images(output_dir)
    except Exception as e:
        print(f"Erro ao processar a imagem {image_path}: {str(e)}")
        
    return sprite_coordinates

def process_directory(directory):
    print(f"Processando {directory}...")
    sprite_sheets_dir = "sprite_sheets"
    training_data_dir = "training_data"
    subdir_path = os.path.join(sprite_sheets_dir, directory)
    output_dir = os.path.join(training_data_dir, directory)
    os.makedirs(output_dir, exist_ok=True)

    png_files = [f for f in os.listdir(subdir_path) if f.endswith('.png')]
    if not png_files:
        print(f"No PNG file found in {subdir_path}")
        return
    image_path = os.path.join(subdir_path, png_files[0])

    sprite_data = extract_sprite_coordinates_from_sheet(image_path, output_dir)
    json_filename = os.path.join(output_dir, 'data.json')
    with open(json_filename, 'w') as json_file:
        json.dump(sprite_data, json_file, indent=4)

def main():

    # Início da contagem do tempo
    start_time = time.time()

    if os.path.exists('training_data'):
        shutil.rmtree('training_data')

    sprite_sheets_dir = "sprite_sheets"
    directories = [item for item in os.listdir(sprite_sheets_dir) if os.path.isdir(os.path.join(sprite_sheets_dir, item))]

    with ThreadPoolExecutor(max_workers=12) as executor:
        executor.map(process_directory, directories)

    # Fim da contagem do tempo
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Script executado em: {elapsed_time:.2f} segundos.")

if __name__ == "__main__":
    
    # faça com que o script pare quando o usuário pressionar Ctrl + C
    try:
        main()
    except KeyboardInterrupt:
        print("Script interrompido pelo usuário.")
    