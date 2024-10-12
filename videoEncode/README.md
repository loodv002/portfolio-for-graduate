# File to Video

## Usage
* To convert a file into video: `$ python ftv.py <file_to_encode>`
* To reproduce a file from video: `$ python vtf.py <video_file_to_decode>`

## Important Note
* The file structure in the `v1` and `v2` directories are the same. The difference between the two versions is that `v2` employs the [7,4] Hamming code for error correction, while `v1` does not.
* The `UNIT_WIDTH` parameter in `const.py` determines the width of color blocks in pixels for the output video. The value will affect the error rate, encoding speed, and output file size. Check "`UNIT_WIDTH` Selection" section for details.

## How It Works
* **File to Video:**
  * Each input bit is represented by a black or white block. All the color blocks will be placed sequentially, frame by frame.
  * If error correction is employed, parity bits will be added before conversion into color blocks.
  
* **Video to File:**
  * For an input video file, the middle color of each block is sampled and converted back into bit stream.
  * By sampling the middle of each block, we reduce errors caused by neighboring blocks.

## `UNIT_WIDTH` Selection
* The value should be a factor of both `VIDEO_HEIGHT` and `VIDEO_WIDTH` defined in the same file.
* A larger `UNIT_WIDTH` has the following impacts:
  * A smaller error rate.
  * A smaller output file size.
  * A longer encoding time.

## Version and Parameter Suggestions
* If the video will not be compressed during storage or transmission, `v1` with `UNIT_WIDTH=2` is sufficient.
* If you plan to store or transmit the video via platforms such as YouTube, video compression is inevitable. 
  * For `v1`, `UNIT_WIDTH=8` should still work properly under reasonable levels of compression. However, due to the larger block width, the encoding process will take significantly more time.
  * For `v2` (with error correction), `UNIT_WIDTH=4` consistently ensures data correctness but will result in a larger output video.