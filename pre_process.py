import os
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import img_to_array
from shutil import copy2
import random

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TRAINING_DATA_DIR = os.path.join(BASE_DIR, "training_data")
VALIDATION_DATA_DIR = os.path.join(BASE_DIR, "validation_data")

TARGET_SIZE = (128, 128)


def prepare_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, TARGET_SIZE)
    image = img_to_array(image) / 255.0
    return image


def copy_negative_images(target_dir, num_samples):
    negatives_path = os.path.join(TRAINING_DATA_DIR, 'negatives')

    all_negative_files = [f for f in os.listdir(
        negatives_path) if f.endswith('.png')]

    sampled_negatives = random.sample(
        all_negative_files, min(num_samples, len(all_negative_files)))
    for f in sampled_negatives:
        copy2(os.path.join(negatives_path, f), os.path.join(target_dir, f))


if __name__ == "__main__":
    subdirectories = [d for d in os.listdir(TRAINING_DATA_DIR) if os.path.isdir(
        os.path.join(TRAINING_DATA_DIR, d)) and d != "negatives"]

    for subdir in subdirectories:
        subdir_path = os.path.join(TRAINING_DATA_DIR, subdir)
        all_files = [f for f in os.listdir(subdir_path) if f.endswith('.png')]

        # Verifique se há mais de 1 imagem para dividir em conjuntos de treino e teste
        if len(all_files) > 1:
            train_files, val_files = train_test_split(
                all_files, test_size=0.2, random_state=42)

            # Copy train files to the correct directory
            for file in train_files:
                src_path = os.path.join(subdir_path, file)
                dest_path = os.path.join(TRAINING_DATA_DIR, subdir, file)
                if src_path != dest_path:
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    copy2(src_path, dest_path)
            copy_negative_images(TRAINING_DATA_DIR, len(train_files))

            # Copy validation files to the correct directory
            for file in val_files:
                src_path = os.path.join(subdir_path, file)
                dest_path = os.path.join(VALIDATION_DATA_DIR, subdir, file)
                if src_path != dest_path:
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    copy2(src_path, dest_path)
            copy_negative_images(VALIDATION_DATA_DIR, len(val_files))

        # Caso contrário, coloque a única imagem no conjunto de treino
        else:
            for file in all_files:
                src_path = os.path.join(subdir_path, file)
                dest_path = os.path.join(TRAINING_DATA_DIR, subdir, file)
                if src_path != dest_path:
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    copy2(src_path, dest_path)
            copy_negative_images(TRAINING_DATA_DIR, len(all_files))

    print("Processamento concluído!")
