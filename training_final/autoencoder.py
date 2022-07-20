from keras import Input, Model
from keras.layers import Conv2D, MaxPooling2D, UpSampling2D

width = 544
height = 352


def create():
    input = Input(shape=(height, width, 1))

    x = Conv2D(32, (3, 3), activation='relu', padding='same')(input)
    x = MaxPooling2D((2, 2), padding='same')(x)

    x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

    # Autoencoder
    return Model(input, x)
