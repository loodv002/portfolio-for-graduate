from const import *
import sys
import os
import numpy as np
import cv2
import ffmpegcv
import struct
import tqdm
from pathlib import Path

BYTE_RIGHT_SHIFT = np.arange(7, -1, -1, dtype=np.uint8)
G = np.array([
    [1, 1, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 0, 0, 1, 0],
], dtype=np.uint8)

def writeToVideo(video, bytes):
    bytes_ = np.frombuffer(bytes, np.uint8)
    bytes_ = np.pad(bytes_, (0, BYTE_PER_PAGE - len(bytes_)), mode='constant', constant_values=0)
    bytes_ = bytes_.reshape((BYTE_PER_PAGE, 1))
    bits = (bytes_.repeat(8, axis=1) >> BYTE_RIGHT_SHIFT) & 1
    bits = bits.reshape((BYTE_PER_PAGE * 2, 4))
    
    withParity = bits @ G
    frame = np.zeros_like(withParity, dtype=np.uint8)
    frame[withParity == 1] = 255
    frame = frame.reshape((UNIT_PER_FRAME_HEIGHT, UNIT_PER_FRAME_WIDTH, 1))
    frame = frame.repeat(3, axis=2)
    frame = np.repeat(frame, UNIT_WIDTH, axis=0)
    frame = np.repeat(frame, UNIT_WIDTH, axis=1)
    video.write(frame)

if len(sys.argv) <= 1:
    print('Usage: ftv.py <file_to_encode>')
    exit(1)

inputFilePath = sys.argv[1]
inputFileName = Path(inputFilePath).name
outputFileName = f'{Path(inputFilePath).name}.mp4'

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = ffmpegcv.VideoWriter(outputFileName, 'h264', 30)
remainFileSize = inputFileSize = os.path.getsize(inputFilePath)

print(f'Size: {inputFileSize}')

metaData = b''.join([
    struct.pack('!Q', inputFileSize) + 
    struct.pack('!B', len(inputFileName)) + 
    inputFileName.encode()
])
writeToVideo(video, metaData)

progressBar = tqdm.tqdm(total=inputFileSize)
with open(inputFilePath, 'rb') as inputFile:
    while remainFileSize > 0:
        page = inputFile.read(BYTE_PER_PAGE)
        writeToVideo(video, page)

        remainFileSize -= len(page)
        progressBar.update(len(page))

video.release()