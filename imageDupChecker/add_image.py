import os
from pathlib import Path
import cv2
import numpy as np

import image_utils
from image_db.utils import addRecord, recordExist
import bin_square_compress as bsc

def addImage(imagePath: str):
    assert os.path.exists(imagePath)
    imagePath = os.path.abspath(imagePath)

    image = image_utils.readImage(imagePath)
    
    resizedImage = image_utils.toWidthSquare(image)
    binaryBitmap = image_utils.toBinary(resizedImage)

    counts = image_utils.countGrid(binaryBitmap)

    compressedBitmap = bsc.compress(binaryBitmap)
    
    baseDir = os.path.dirname(os.path.abspath(__file__))
    bitmapPath = f'{baseDir}/bitmap/{Path(imagePath).stem}'

    with open(bitmapPath, 'wb') as bitmapFile:
        bitmapFile.write(compressedBitmap)

    if recordExist(imagePath):
        print('image already in DB')
    else:
        addRecord(imagePath, bitmapPath, counts)

if __name__ == '__main__':
    from sys import argv
    if len(argv) <= 1:
        print('Usage: ./add_image.py <image path>')
        exit(1)
    
    addImage(argv[1])