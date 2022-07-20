import glob

import numpy as np
import cv2
from matplotlib import pyplot as plt
from scipy.linalg._decomp_schur import eps


path = 'train/2.png'



def method1():
    img = cv2.imread(path)
    dst = cv2.fastNlMeansDenoising(img,None, h=7)
    plt.subplot(121)
    plt.imshow(img)
    plt.subplot(122)
    plt.imshow(dst)
    plt.show()



def method2():
    for filename in sorted(glob.glob('test' + '/*.png')):
        st_img = cv2.imread(filename)
        img = cv2.imread(filename)
        blur = cv2.medianBlur(img, 5)
        foreground = img.astype("float") - blur
        foreground[foreground > 0] = 0
        # range [0, 1]
        minVal = np.min(foreground)
        maxVal = np.max(foreground)
        foreground = (foreground - minVal) / (maxVal - minVal + eps)
        foreground = foreground * 255.
        cv2.imwrite('predicted_open/' + filename[5:], foreground)
        # cv2.imshow('before', st_img)
        # cv2.imshow('after', foreground)
        # cv2.waitKey()


method2()