import cv2
import os

from typing import List, Tuple

from image_db.utils import getRecordByCounts
from image_db.model import ImageRecord
import image_utils
from image_utils import WIDTH
import bin_square_compress as bsc

BITMAP_DIFFERENT_THRESHOLD = 10000

def queryImage(imagePath: str) -> List[Tuple[ImageRecord, int]]:
    assert os.path.exists(imagePath)
    
    image = image_utils.readImage(imagePath)

    resizedImage = image_utils.toWidthSquare(image)
    binaryBitmap = image_utils.toBinary(resizedImage)

    counts = image_utils.countGrid(binaryBitmap)
    compressedBitmap = bsc.compress(binaryBitmap)

    queryResult = []
    for record in getRecordByCounts(counts):
        with open(record.bitmapPath, 'rb') as recordCompressedBitmapFile:
            recordCompressedBitmap = recordCompressedBitmapFile.read()
        
        difference = bsc.compare(recordCompressedBitmap, compressedBitmap, WIDTH)
        if difference < BITMAP_DIFFERENT_THRESHOLD: 
            queryResult.append((record.imagePath, difference))

    queryResult.sort(key=lambda tup: tup[1])
    return queryResult


if __name__ == '__main__':
    from sys import argv
    if len(argv) <= 1:
        print('Usage: ./query_image.py <image path>')
        exit(1)
    
    print(queryImage(argv[1]))