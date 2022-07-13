import numpy as np
from PIL import Image
from keras.saving.model_config import model_from_json
from keras_preprocessing.image import load_img, img_to_array

width = 544
height = 352

def load_image(path):
    img = load_img(path, color_mode='grayscale', target_size=(height, width))  # loading the image
    img = img.convert('L')
    in_height = img.height
    in_width = img.width
    img = img_to_array(img, dtype='float32') / 255.  # converting the image to array and normalizing the data
    return np.array(img), in_width, in_height

def predict(path):

    json_file = open("media/model/autoencoder_documents.json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("media/model/autoencoder_documents_weights.h5")

    loaded_model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    test_data, in_width, in_height = load_image(path[1:])
    test_data = np.asarray(test_data).astype('float32').reshape(-1, height, width, 1)
    predictions = loaded_model.predict(test_data)

    r_im = predictions[0].reshape(height, width)
    im = Image.fromarray(r_im * 255)
    im = im.resize((in_width, in_height))
    return im