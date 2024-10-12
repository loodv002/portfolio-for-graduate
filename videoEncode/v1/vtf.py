import scipy.stats
from const import *
import sys
import os
import numpy as np
import scipy
import cv2
import struct
import tqdm

from utils import *
from const import *

if len(sys.argv) <= 1:
    print('Usage: vtf.py <video_to_decode>')
    exit(1)

BYTE_RIGHT_SHIFT = np.arange(8, dtype=np.uint8)
BYTE_LEFT_SHIFT = np.arange(7, -1, -1, dtype=np.uint8)

def frameToBytes(frame):
    half = UNIT_WIDTH // 2
    singleColor = np.array(frame[half:VIDEO_HEIGHT:UNIT_WIDTH,half:VIDEO_WIDTH:UNIT_WIDTH,:], dtype=np.uint16)
    singleColor = singleColor.sum(axis=2)
    singleColor = singleColor.reshape((UNIT_PER_PAGE // 8, 8))
    bits = np.zeros_like(singleColor, dtype=np.uint8)
    bits[singleColor <= 382] = 0
    bits[singleColor > 382] = 1
    bits = bits << BYTE_LEFT_SHIFT
    bytes_ = np.bitwise_or.reduce(bits, axis=1)
    return bytes(bytes_)

inputVideoPath = sys.argv[1]
video = cv2.VideoCapture(inputVideoPath)
nFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

ok, frame = video.read()
metaData = frameToBytes(frame)
outputFileSize, = struct.unpack('!Q', metaData[:8])
outputFileNameLength, = struct.unpack('!B', metaData[8:9])
outputFileName = f'recreate_{metaData[9:9+outputFileNameLength].decode()}'
outputFileName = uniquify(outputFileName)

print(f'File name: {outputFileName}')
print(f'File size: {outputFileSize}')

remainFileSize = outputFileSize
progressBar = tqdm.tqdm(total = nFrames-1)
with open(outputFileName, 'wb') as outputFile:
    while remainFileSize >= 0:
        ok, frame = video.read()
        if not ok: break
        page = frameToBytes(frame)[:remainFileSize]
        outputFile.write(page)

        remainFileSize -= len(page)
        progressBar.update()

video.release()