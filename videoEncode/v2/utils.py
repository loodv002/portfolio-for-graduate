import os
from pathlib import Path

def uniquify(filePath):
    fileName = Path(filePath).stem
    extension = Path(filePath).suffix
    path = str(Path(filePath).parent)
    if not os.path.exists(filePath): return filePath
    i = 1
    while os.path.exists(f'{path}/{fileName} ({i}){extension}'): i += 1
    return f'{path}/{fileName} ({i}){extension}'