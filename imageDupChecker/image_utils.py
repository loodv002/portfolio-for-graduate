import numpy as np
import imutils
import cv2

from typing import List

WIDTH = 512

def readImage(imagePath: str) -> np.ndarray:
    # Note: cv2.imread() will fail for chinese pathname
    return cv2.imdecode(np.fromfile(file=imagePath, dtype=np.uint8), cv2.IMREAD_COLOR)

def toWidthSquare(image: np.ndarray) -> np.ndarray:
    '''Resize numpy image into WIDTH x WIDTH

    :param image: image in np.ndarray
    :return: resized image in np.ndarray, with shape (WIDTH, WIDTH, 3)
    '''
    # if image.shape[0] > image.shape[1]:
    #     resized = imutils.resize(image, height=WIDTH)
    # else:
    #     resized = imutils.resize(image, width=WIDTH)
        
    # if resized.shape[0] < WIDTH: 
    #     resized = np.vstack([resized, np.zeros((WIDTH - resized.shape[0], resized.shape[1], 3))])
    # if resized.shape[1] < WIDTH: 
    #     resized = np.hstack([resized, np.zeros((WIDTH, WIDTH - resized.shape[1], 3))])
    # return resized
    return cv2.resize(image, (WIDTH, WIDTH), interpolation=cv2.INTER_AREA)

def toBinary(image: np.ndarray) -> np.ndarray:
    '''Generate binary bitmap by image.

    :param image: image in np.ndarray
    :return: binary bitmap in np.ndarray
    '''
    h, w, _ = image.shape
    binary = np.zeros((h, w), dtype=np.uint8)
    binary[image.sum(axis=-1) > 382] = 1
    return binary

def countGrid(binary: np.ndarray) -> List[int]:
    '''Count number of bit 1 in each grid.

    :param binary: binary bitmap in np.ndarray
    :return: a list of count value
    '''
    counts = []
    w = WIDTH // 4
    for i in range(4):
        for j in range(4):
            counts.append(int(binary[i*w:i*w+w,j*w:j*w+w].sum()))
    return counts
