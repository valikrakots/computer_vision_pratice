import glob

from PIL import Image

import autoencoder as a
import numpy as np
import transforms
from keras.utils import load_img, img_to_array


def numeric_comparison(item):
    a = (item.split('.')[0]).split('/')[1]
    return int(a)


def load_images(path):
    images = []
    for filename in sorted(glob.glob(path + '/*.png'), key=numeric_comparison):
        img = load_img(filename, color_mode='grayscale',
                       target_size=(a.height, a.width))  # loading the image
        img = img_to_array(img, dtype='float32') / 255.  # converting the image to array and normalizing the data
        images.append(img)
    return images


def prepare_simple(train, train_cleaned):
    train_data_all = np.array(load_images(train))
    train_cleaned_data_all = np.array(load_images(train_cleaned))
    train_data = train_data_all[:120]
    train_cleaned_data = train_cleaned_data_all[:120]
    val_train_data = train_data_all[120:]
    val_train_cleaned_data = train_cleaned_data_all[120:]
    return train_data, train_cleaned_data, val_train_data, val_train_cleaned_data


def prepare_one_transform(train, train_cleaned):
    all_data = load_images(train)
    all_cleaned_data = load_images(train_cleaned)
    train_data = all_data[:120]
    train_cleaned_data = all_cleaned_data[:120]
    val_train_data = all_data[120:144]
    val_train_cleaned_data = all_cleaned_data[120:144]
    train_data_copy = train_data.copy()
    for image in train_data_copy:
        augmented = img_to_array((transforms.first(image=image)["image"]))
        train_data.append(augmented)

    train_cleaned_data_copy = train_cleaned_data.copy()
    for image in train_cleaned_data_copy:
        train_cleaned_data.append(image)

    return np.array(train_data), np.array(train_cleaned_data), np.array(val_train_data), np.array(
        val_train_cleaned_data)


def prepare_two_transforms(train, train_cleaned):
    all_data = load_images(train)
    all_cleaned_data = load_images(train_cleaned)
    train_data = all_data[:120]
    train_cleaned_data = all_cleaned_data[:120]
    val_train_data = all_data[120:144]
    val_train_cleaned_data = all_cleaned_data[120:144]
    train_data_copy = train_data.copy()
    for image in train_data_copy:
        augmented = img_to_array((transforms.first(image=image)["image"]))
        train_data.append(augmented)
    for image in train_data_copy:
        augmented = img_to_array((transforms.second(image=image)["image"]))
        train_data.append(augmented)

    train_cleaned_data_copy = train_cleaned_data.copy()
    for image in train_cleaned_data_copy:
        train_cleaned_data.append(image)
    for image in train_cleaned_data_copy:
        train_cleaned_data.append(image)

    return np.array(train_data), np.array(train_cleaned_data), np.array(val_train_data), np.array(
        val_train_cleaned_data)


def load_test_images(path):
    images = []
    sizes = []
    names = []
    for filename in sorted(glob.glob(path + '/*.png'), key=numeric_comparison):
        img = load_img(filename, color_mode='grayscale')  # loading the image
        sizes.append([img.height, img.width])
        names.append(filename[5:])

        img = img.resize((a.width, a.height), Image.ANTIALIAS)
        img = img_to_array(img, dtype='float32') / 255.  # converting the image to array and normalizing the data
        images.append(np.asarray(img).astype('float32').reshape(-1, a.height, a.width, 1))

    return images, sizes, names
