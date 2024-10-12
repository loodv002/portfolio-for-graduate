VIDEO_HEIGHT = 1080
VIDEO_WIDTH = 1920

UNIT_WIDTH = 4
UNIT_PER_FRAME_WIDTH = VIDEO_WIDTH // UNIT_WIDTH
UNIT_PER_FRAME_HEIGHT = VIDEO_HEIGHT // UNIT_WIDTH
UNIT_PER_PAGE = UNIT_PER_FRAME_WIDTH * UNIT_PER_FRAME_HEIGHT

BYTE_PER_PAGE = UNIT_PER_PAGE // 8 // 2

assert VIDEO_HEIGHT % UNIT_WIDTH == 0
assert VIDEO_WIDTH % UNIT_WIDTH == 0