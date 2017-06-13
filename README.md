# Seam Carving
Seam carving is an algorithm for content-aware image resizing.  
Photos can represented as a grid of pixels. Paths (top to bottom or left to right) of the grid that represent pixels which hold the least significance to the meaning of the photo are called seams.  
The algorithm reduces the dimensions of the input image by removing one seam at a time until the desired dimensions are reached.  
Although this implementation reduces the size of the photo, seam carving can also be used to increase the size of a photo.

## Running the script
###### Dependencies
  * [NumPy](http://www.numpy.org/)
  * [OpenCV](http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_tutorials.html)

###### Basic usage
`python run.py -s [path to source image] -o [path to output image] -x [desired width] -y [desired height]`

###### Example usage
`python run.py -s test_images/test5/source.png -o test_images/test5/out.png -x 580 -y 414`

# Results
###### Test 5 source with x = 600, y = 414
![alt text](https://github.com/g3aishih/seam-carving/blob/master/test_images/test5/source.jpg "Test 5 source")

###### Test 5 result with x = 580, y = 414
![alt text](https://github.com/g3aishih/seam-carving/blob/master/test_images/test5/out.png "Test 5 result")
