# Seam Carving
Seam carving is an algorithm for content-aware image resizing.

Photos can represented as a grid of pixels. Paths (top to bottom or left to right) of the grid that represent pixels with the least significance to the photo are called seams.

The algorithm reduces the dimensions of the input image by removing one seam at a time until the desired dimensions are reached.

## Running the script
###### Dependencies
  * [NumPy](http://www.numpy.org/)
  * [OpenCV](http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_tutorials.html)

###### Basic usage
`python run.py -s [path to source image] -o [path to output image] -x [desired width] -y [desired height]`

###### Example usage
`python run.py -s test_images/test2/source.jpg -o test_images/test2/out.png -x 500 -y 606`

## Results
###### Test 2 source with x = 600, y = 606
![alt text](https://github.com/g3aishih/seam-carving/blob/master/test_images/test2/source.jpg "Test 2 source")

###### Test 2 seams cut
![alt text](https://github.com/g3aishih/seam-carving/blob/master/test_images/test2/out_seams.png "Test 2 seams")


###### Test 2 result with x = 500, y = 606
![alt text](https://github.com/g3aishih/seam-carving/blob/master/test_images/test2/out.png "Test 2 result")
