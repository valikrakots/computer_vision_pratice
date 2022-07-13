import glob

import numpy as np
from keras import Input, Model
from keras.layers import Conv2D, MaxPooling2D, UpSampling2D
from keras.utils import load_img, img_to_array
from keras.metrics import MeanSquaredError, RootMeanSquaredError, MeanSquaredLogarithmicError

width = 544
height = 352


def numeric_comparison(item):
    a = (item.split('.')[0]).split('/')[1]
    return int(a)


def load_images(path):
    images = []
    for filename in sorted(glob.glob(path + '/*.png'), key=numeric_comparison):
        img = load_img(filename, color_mode='grayscale', target_size=(height, width))  # loading the image
        img = img_to_array(img, dtype='float32') / 255.  # converting the image to array and normalizing the data
        images.append(img)
    return np.array(images)


train_data_all = load_images('train')
train_cleaned_data_all = load_images('train_cleaned')
train_data = train_data_all[:120]
train_cleaned_data = train_cleaned_data_all[:120]
val_train_data = train_data_all[120:]
val_train_cleaned_data = train_cleaned_data_all[120:]

input = Input(shape=(height, width, 1))

x = Conv2D(32, (3, 3), activation='relu', padding='same')(input)
x = MaxPooling2D((2, 2), padding='same')(x)

x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

autoencoder = Model(input, x)
autoencoder.compile(optimizer="adam", loss="mse",
                    metrics=[MeanSquaredError(), RootMeanSquaredError(), MeanSquaredLogarithmicError()])
autoencoder.summary()

autoencoder.fit(
    train_data,
    train_cleaned_data,
    epochs=20,
    batch_size=8,
    shuffle=True,
    validation_data=(val_train_data, val_train_cleaned_data),
)

model_json = autoencoder.to_json()
json_file = open("autoencoder_documents.json", "w")
json_file.write(model_json)
json_file.close()
autoencoder.save_weights("autoencoder_documents_weights.h5")
print("The network saved completely")
