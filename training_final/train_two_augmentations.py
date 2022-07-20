import prepare_data
import autoencoder as a
import metrics
from keras.callbacks import EarlyStopping
from keras.metrics import MeanSquaredError, RootMeanSquaredError

epochs = 50
batch_size = 8

train_data, train_cleaned_data, val_train_data, val_train_cleaned_data = prepare_data.prepare_two_transforms('train', 'train_cleaned')

autoencoder = a.create()
autoencoder.compile(optimizer="adam", loss="mse",
                    metrics=[MeanSquaredError(), RootMeanSquaredError(), metrics.PSNR, metrics.SSIM,
                             metrics.MULTISCALESSIM])
autoencoder.summary()

early_stop = EarlyStopping(monitor="val_loss", patience=3, verbose=1)
callbacks_list = [early_stop, ]

autoencoder.fit(
    train_data,
    train_cleaned_data,
    epochs=epochs,
    batch_size=batch_size,
    shuffle=True,
    validation_data=(val_train_data, val_train_cleaned_data),
    callbacks=callbacks_list,
)

model_json = autoencoder.to_json()
json_file = open("models/autoencoder_two_aug.json", "w")
json_file.write(model_json)
json_file.close()
autoencoder.save_weights("autoencoder_two_aug.h5")
print("The network saved completely")
