import os
import cv2 as cv
import numpy as np
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator

from keras._tf_keras.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

# Define the paths
frames_folder = '/Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src/frames'  # Adjust this to your frames folder path

# /Users/benayah/Desktop/Code/Sec_camera_project/face_reco_v4/face_reco_v4_v2/src/frames


# Function to load images from a structured directory
def load_images_from_directory(directory):
    images = []
    labels = []
    label_dict = {}

    for user_folder in os.listdir(directory):
        user_path = os.path.join(directory, user_folder)
        if os.path.isdir(user_path):
            for region_folder in os.listdir(user_path):
                region_path = os.path.join(user_path, region_folder)
                if os.path.isdir(region_path):
                    for img_name in os.listdir(region_path):
                        img_path = os.path.join(region_path, img_name)
                        img = cv.imread(img_path)
                        img = cv.resize(img, (128, 128))  # Resize images
                        images.append(img)
                        labels.append(user_folder)  # Use user folder name as label

    return np.array(images), np.array(labels)

def train():
    # Load images
    X, y = load_images_from_directory(frames_folder)

    # Normalize the image data
    X = X.astype('float32') / 255.0

    # Convert labels to numerical values
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # One-hot encode the labels
    y_one_hot = to_categorical(y_encoded)

    # Define the CNN model
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(len(np.unique(y)), activation='softmax'))  # Adjust output layer for the number of classes

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Data augmentation
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    # Fit the model
    model.fit(datagen.flow(X, y_one_hot, batch_size=32), epochs=50)

    # Save the model
    model.save('face_recognition_model.h5')
    np.save('classes.npy', label_encoder.classes_)
