import tensorflow as tf


def PSNR(y_true, y_pred):
    return tf.image.psnr(y_true, y_pred, 1.0)

def SSIM(y_true, y_pred):
    return tf.image.ssim(y_true, y_pred, 1.0)

def MULTISCALESSIM(y_true, y_pred):
    return tf.image.ssim_multiscale(y_true, y_pred, 1.0)