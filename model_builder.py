import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_DATA_DIR = os.path.join(SCRIPT_DIR, 'training_data')
VALIDATION_DATA_DIR = os.path.join(SCRIPT_DIR, 'validation_data')
IMG_SIZE = 128

# Data Augmentation para o conjunto de treinamento
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Verifica as classes presentes no conjunto de treinamento e no conjunto de validação
train_classes = os.listdir(TRAINING_DATA_DIR)
validation_classes = os.listdir(VALIDATION_DATA_DIR)
classes_to_remove = set(train_classes) - set(validation_classes)
if classes_to_remove:
    print(f"Removendo as classes {classes_to_remove} do conjunto de treinamento")
    for class_to_remove in classes_to_remove:
        class_path = os.path.join(TRAINING_DATA_DIR, class_to_remove)
        if os.path.isfile(class_path):
            os.remove(class_path)
        else:
            shutil.rmtree(class_path)
    train_classes = os.listdir(TRAINING_DATA_DIR)

# Cria os geradores de fluxo de dados de treinamento e validação
train_generator = train_datagen.flow_from_directory(
    TRAINING_DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=32,
    class_mode='categorical',
    classes=train_classes
)

validation_generator = train_datagen.flow_from_directory(
    VALIDATION_DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=32,
    class_mode='categorical',
    classes=train_classes
)

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(len(train_classes), activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=30,
    verbose=1
)

val_loss, val_acc = model.evaluate(validation_generator, verbose=1)
print(f"Validation accuracy: {val_acc * 100:.2f}%")

model.save('model.h5')