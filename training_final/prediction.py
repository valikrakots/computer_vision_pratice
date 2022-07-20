from PIL import Image
from keras.saving.model_config import model_from_json
import prepare_data
import autoencoder as a


def predict():
    json_file = open("models/autoencoder_two_aug.json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("models/autoencoder_two_aug.h5")

    loaded_model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    test_data, sizes, names = prepare_data.load_test_images('test')

    for i in range(0, len(test_data)):
        image = loaded_model.predict(test_data[i])
        r_im = image.reshape(a.height, a.width)
        im = Image.fromarray(r_im * 255)
        im = im.resize((sizes[i][1], sizes[i][0]))
        im = im.convert(mode='L')
        im.save('predicted/' + names[i])


predict()