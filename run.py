# Shihan Ai
# Github: g3aishih

import numpy as np
import cv2 as cv
import sys, os, argparse
from util import *

class SeamCarve:
    def __init__(self, source, width, height):
        self.source = source
        self.colorImage = source.copy()
        self.outX = width
        self.outY = height
        self.verticalSeamsLeft = source.shape[1] - width
        self.horizontalSeamsLeft = source.shape[0] - height

    def run(self):
        cutVertical = True
        print("Original image size: (%d, %d)" % (self.colorImage.shape[1], self.colorImage.shape[0]))
        while (self.verticalSeamsLeft > 0 or self.horizontalSeamsLeft > 0):
            if cutVertical:
                if self.verticalSeamsLeft > 0:
                    self.colorImage = self.cutVertical()
                    print("Reduced size to: (%d, %d)" % (self.colorImage.shape[1], self.colorImage.shape[0]))
                cutVertical = False
            else:
                if self.horizontalSeamsLeft > 0:
                    self.colorImage = self.cutHorizontal()
                    print("Reduced size to: (%d, %d)" % (self.colorImage.shape[1], self.colorImage.shape[0]))
                cutVertical = True
        return self.colorImage

    def cutVertical(self):
        minSeam = np.inf
        minSeamIndex = 0

        # Create a placeholder for the resized image
        result = np.zeros((self.colorImage.shape[0], self.colorImage.shape[1] - 1, self.colorImage.shape[2]), dtype=np.uint8)
        imageGray = cv.cvtColor(self.colorImage, cv.COLOR_BGR2GRAY)

        # Calculate the gradient of the image
        # This is used to determine the cost or significance of a pixel
        Dy = cv.Scharr(imageGray, cv.CV_64F, 0, 1)
        Dx = cv.Scharr(imageGray, cv.CV_64F, 1, 0)
        m = np.sqrt(np.square(Dx) + np.square(Dy)).astype(np.uint8)

        # Build a NxM matrix where each element corresponds to a pixel in the NxM image
        # The matrix holds the mininum cost required to travel to the corresponding pixels
        s = np.zeros_like(m, dtype=np.uint16)

        # We travel from the top row of the image so we initialize the cost of the
        # first row of our cost matrix as the gradient values of the first row of pixels
        s[0] = m[0]

        for y in range(1, s.shape[0]):
            for x in range(s.shape[1]):
                if x == 0:
                    s[y,x] = m[y,x] + np.min(s[y-1,x:x+2])
                elif x == s.shape[1] - 1:
                    s[y,x] = m[y,x] + np.min(s[y-1,x-1:x+1])
                else:
                    s[y,x] = m[y,x] + np.min(s[y-1,x-1:x+2])

                # Locate the pixel in the bottom row with the smallest cost
                # This pixel is the end of our seam
                if y == s.shape[0] - 1:
                    if s[y,x] < minSeam:
                        minSeam = s[y,x]
                        minSeamIndex = x

        # Starting from the end of the seam, traverse back to the top of the
        # matrix to determine the other pixels in the seam.
        # Copy pixels that are not in the seam into the placeholder image
        x = minSeamIndex
        for y in range(s.shape[0] - 1, -1, -1):
            if y > 0:
                if x == 0:
                    x = np.argmin(s[y-1,x:x+2])
                elif x == s.shape[1] - 1:
                    x = x - (1 - np.argmin(s[y-1,x-1:x+1]))
                else:
                    x = x + np.argmin(s[y-1,x-1:x+2]) - 1
            result[y,:] = np.append(self.colorImage[y,:x], self.colorImage[y,x+1:], axis=0)
        self.verticalSeamsLeft -= 1
        return result

    def cutHorizontal(self):
        # Follows the same procedure as the cutVertical function but cuts seams
        # horizontally instead of vertically
        minSeam = np.inf
        minSeamIndex = 0
        result = np.zeros((self.colorImage.shape[0] - 1, self.colorImage.shape[1], self.colorImage.shape[2]), dtype=np.uint8)
        imageGray = cv.cvtColor(self.colorImage, cv.COLOR_BGR2GRAY)

        Dy = cv.Scharr(imageGray, cv.CV_64F, 0, 1)
        Dx = cv.Scharr(imageGray, cv.CV_64F, 1, 0)

        m = np.sqrt(np.square(Dx) + np.square(Dy)).astype(np.uint8)
        s = np.zeros_like(m, dtype=np.uint16)
        s[:,0] = m[:,0]

        for x in range(1, s.shape[1]):
            for y in range(s.shape[0]):
                if y == 0:
                    s[y,x] = m[y,x] + np.min(s[y:y+2,x-1])
                elif y == s.shape[0] - 1:
                    s[y,x] = m[y,x] + np.min(s[y-1:y+1,x-1])
                else:
                    s[y,x] = m[y,x] + np.min(s[y-1:y+2,x-1])
                if x == s.shape[1] - 1:
                    if s[y,x] < minSeam:
                        minSeam = s[y,x]
                        minSeamIndex = y

        y = minSeamIndex
        for x in range(s.shape[1] - 1, -1, -1):
            if x > 0:
                if y == 0:
                    y = np.argmin(s[y:y+2,x-1])
                elif y == s.shape[0] - 1:
                    y = y - (1 - np.argmin(s[y-1:y+1,x-1]))
                else:
                    y = y + np.argmin(s[y-1:y+2,x-1]) - 1
            result[:,x] = np.append(self.colorImage[:y,x], self.colorImage[y+1:,x], axis=0)
        self.horizontalSeamsLeft -= 1
        return result

def main(args):
    source = readSource(args.s)
    try:
        assert source is not None
    except:
        print("Could not read source image")
        return

    try:
        assert args.x > 0 and args.x <= source.shape[1]
        assert args.y > 0 and args.y <= source.shape[0]
    except:
        print("Invalid target dimensions\nDimensions must be positive and smaller than or equal to the image's original dimensions")
        return

    seamCarve = SeamCarve(source, args.x, args.y)
    result = seamCarve.run()

    debug(result)
    writeImage(args.o, result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        type=str,
                        help='Path to source image',
                        required=True)
    parser.add_argument('-o',
                        type=str,
                        help='Path to output image',
                        required=True)
    parser.add_argument('-x',
                        type=int,
                        default=0,
                        help='Desired width of output',
                        required=True)
    parser.add_argument('-y',
                        type=int,
                        default=0,
                        help='Desired height of output',
                        required=True)
    args = parser.parse_args()

    t1 = t2 = 0
    t1 = cv.getTickCount()
    main(args)
    t2 = cv.getTickCount()
    print('Completed in %g seconds'%((t2-t1)/cv.getTickFrequency()))
