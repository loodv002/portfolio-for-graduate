import numpy as np
from typing import Literal, Dict, Tuple

class BitWriter:
    def __init__(self):
        self.bytes = []
        self.trailing = 0
        self.trailingLen = 0
    def write(self, b: Literal[0, 1]):
        self.trailing |= b << (7 - self.trailingLen)
        self.trailingLen += 1

        if self.trailingLen == 8:
            self.bytes.append(self.trailing.to_bytes(1, 'big'))
            self.trailing = 0
            self.trailingLen = 0
    def dumpBytes(self):
        return b''.join(self.bytes) + self.trailing.to_bytes(1, 'big')
    
class BitReader:
    def __init__(self, bytes_: bytes):
        self.bytes = bytes_
        self.idx = 0
    def read(self) -> Literal[0, 1]:
        d, m = divmod(self.idx, 8)
        self.idx += 1
        return (self.bytes[d] >> (7-m)) & 1
    
def compress(binary: np.ndarray):
    '''
    A bit 0: follow by pure 0 or 1.
    A bit 1: follow by mix of 0 and 1.
    '''
    pure: Dict[Tuple[int, int, int], Literal[0, 1, 2]] = {}

    def checkPure(l: int, t: int, w: int) -> Literal[0, 1, 2]:
        key = (l, t, w)
        hw = w // 2
        if w == 1: 
            pure[key] = int(binary[l, t])
            return pure[key]

        childPure = {
            checkPure(l, t, hw),
            checkPure(l, t+hw, hw),
            checkPure(l+hw, t, hw),
            checkPure(l+hw, t+hw, hw)
        }
        if 2 in childPure or len(childPure) > 1:
            pure[key] = 2
            return pure[key]
        pure[key] = list(childPure)[0]
        return pure[key]
    
    def compressPure(l: int, t: int, w: int, bitWriter: BitWriter):
        p = pure[(l, t, w)]
        hw = w // 2

        if p == 2: 
            bitWriter.write(1)
            compressPure(l, t, hw, bitWriter)
            compressPure(l, t+hw, hw, bitWriter)
            compressPure(l+hw, t, hw, bitWriter)
            compressPure(l+hw, t+hw, hw, bitWriter)
        else:
            bitWriter.write(0)
            bitWriter.write(p)

    width = binary.shape[0]
    bitWriter = BitWriter()
    
    checkPure(0, 0, width)
    compressPure(0, 0, width, bitWriter)
    
    return bitWriter.dumpBytes()

def decompress(bytes_: bytes, width: int) -> np.ndarray:
    binary = np.zeros((width, width), np.uint8)
    bitReader = BitReader(bytes_)

    def _decompress(l: int, t: int, w: int, bitReader: BitReader):
        if bitReader.read():
            hw = w // 2
            _decompress(l, t, hw, bitReader)
            _decompress(l, t+hw, hw, bitReader)
            _decompress(l+hw, t, hw, bitReader)
            _decompress(l+hw, t+hw, hw, bitReader)
        else:
            binary[l:l+w,t:t+w] = bitReader.read()

    _decompress(0, 0, width, bitReader)

    return binary

def _generatePure(bytes_: bytes, width: int) -> Dict[Tuple[int, int, int], Literal[0, 1, 2]]:
    pure: Dict[Tuple[int, int, int], Literal[0, 1, 2]] = {}

    def _decompress(l: int, t: int, w: int, bitReader: BitReader):    
        key = (l, t, w)

        if bitReader.read():
            pure[key] = 2
            hw = w // 2
            _decompress(l, t, hw, bitReader)
            _decompress(l, t+hw, hw, bitReader)
            _decompress(l+hw, t, hw, bitReader)
            _decompress(l+hw, t+hw, hw, bitReader)
        else:
            pure[key] = bitReader.read()

    _decompress(0, 0, width, BitReader(bytes_))
    return pure


def compare(bytes1: bytes, bytes2: bytes, width: int) -> int:
    '''Compare between two compressed bitmap

    :param width: square width
    :return: number of difference
    '''
    pure1 = _generatePure(bytes1, width)
    pure2 = _generatePure(bytes2, width)

    def _compare(l: int, t: int, w: int, p1: int, p2: int) -> int:
        key = (l, t, w)
        hw = w // 2

        if p1 == 2: p1 = pure1[key]
        if p2 == 2: p2 = pure2[key]
        
        if p1 == 2 or p2 == 2:
            return (
                _compare(l, t, hw, p1, p2) + 
                _compare(l, t+hw, hw, p1, p2) + 
                _compare(l+hw, t, hw, p1, p2) + 
                _compare(l+hw, t+hw, hw, p1, p2)
            )
        if p1 == p2: return 0
        return w ** 2
    return _compare(0, 0, width, 2, 2)
