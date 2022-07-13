import sys
from functools import cmp_to_key
import keras_ocr

minimal_height = 0


def compare(item1, item2):
    _, box1 = item1
    _, box2 = item2
    x1 = box1[0][0]
    x2 = box2[0][0]
    y1 = box1[0][1]
    y2 = box2[0][1]
    if abs(y1 - y2) <= minimal_height:
        return x1 - x2
    else:
        return y1 - y2


def find_min(prediction):
    min = sys.float_info.max
    for _, box in prediction:
        if box[3][1] - box[0][1] < min:
            min = box[3][1] - box[0][1]
    return min

def convert(path):
    global minimal_height
    # processing image and finding min height of word
    pipeline = keras_ocr.pipeline.Pipeline()
    images = [
        keras_ocr.tools.read(path[1:])
    ]
    prediction_groups = pipeline.recognize(images)
    minimal_height = find_min(prediction_groups[0])

    # sorting result in oder to get text
    predicted_image_1 = sorted(prediction_groups[0], key=cmp_to_key(compare))

    # parsing text
    text = ""
    for str_t, _ in predicted_image_1:
        text += str_t + " "

    return text
