# Image Duplicate Checker

This application focuses on speeding up the process of determining whether or not an image exists in the database. This application will work properly even if the image file has been compressed, scaled, resized, or had its aspect ratio changed. However, it won't consider two images the same if they have been cropped, or had their color significantly altered.

> Note that the application returns candidate images based on abstract infomation (see algorithm section for details). Image comparasion methods should still be employed to determine whether a candidate matches target image.

## Algorithm

### Add Image Record
To add a image into database:
1. Resize it to a fixed square size (`512x512` by default). 
2. Convert it into binary image with only black and white pixels.
   * The binary image is called `bitmap`.
3. Divide bitmap into 4 by 4 grids and count the number of white pixels in each grid. 
4. Record the bitmap files, counts, in `sqlite3` database.

### Query Image Record
To check an image exist or not:
1. Obtain the bitmap using the same steps as for adding an image.
2. Query to database by specifying ranges for each grid count.
3. For each query result, compare its bitmap to the target bitmap, determine similarity by number of different pixels.

### Bitmap Storage
A bitmap is represented by 512x512 bits, which is 32kB. We can further compress it using "Quad-Tree Image Compression", which typically takes less than 5kB to store a bitmap.
> Beacuse of Quad-Tree algorithm, the bitmap most be a square, with a side length that is a power of 2.
