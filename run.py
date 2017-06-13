# Shihan Ai
# Github: g3aishih

import numpy as np
import cv2 as cv
import sys, os, argparse
from util import *

class SeamCarve:
    def __init__(self, source, numSeams):
        self.source = source
        self.colorImage = source.copy()
        self.numSeams = numSeams
        self.seamsCut = 0

    def run_slow(self):
        for i in range(self.numSeams):
            minSeam = np.inf
            minSeamIndex = 0
            result = np.zeros((self.colorImage.shape[0], self.colorImage.shape[1] - 1, self.colorImage.shape[2]), dtype=np.uint8)
            imageGray = cv.cvtColor(self.colorImage, cv.COLOR_BGR2GRAY)

            Dy = cv.Scharr(imageGray, cv.CV_64F, 0, 1)
            Dx = cv.Scharr(imageGray, cv.CV_64F, 1, 0)

            m = np.sqrt(np.square(Dx) + np.square(Dy)).astype(np.uint8)
            s = np.zeros_like(m, dtype=np.uint16)
            s[0] = m[0]

            for y in range(1, s.shape[0]):
                for x in range(s.shape[1]):
                    if x == 0:
                        s[y][x] = m[y][x] + np.min(s[y-1][x:x+2])
                    elif x == s.shape[1] - 1:
                        s[y][x] = m[y][x] + np.min(s[y-1][x-1:x+1])
                    else:
                        s[y][x] = m[y][x] + np.min(s[y-1][x-1:x+2])
                    if y == s.shape[0] - 1:
                        if s[y][x] < minSeam:
                            minSeam = s[y][x]
                            minSeamIndex = x

            x = minSeamIndex
            for y in range(s.shape[0] - 1, -1, -1):
                if y > 0:
                    if x == 0:
                        x = np.argmin(s[y-1][x:x+2])
                    elif x == s.shape[1] - 1:
                        x = x - (1 - np.argmin(s[y-1][x-1:x+1]))
                    else:
                        x = x + np.argmin(s[y-1][x-1:x+2]) - 1
                result[y] = np.append(self.colorImage[y][:x], self.colorImage[y][x+1:], axis=0)
            self.colorImage = result
            self.seamsCut += 1
            print("Seams cut: %d" % (self.seamsCut))
        return self.colorImage

def main(args):
    source = readSource(args.s)
    assert source is not None

    seamCarve = SeamCarve(source, args.c)
    result = seamCarve.run_slow()
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
    parser.add_argument('-c',
                        type=int,
                        default=0,
                        help='Number of seams to cut',
                        required=False)
    args = parser.parse_args()

    t1 = t2 = 0
    t1 = cv.getTickCount()
    main(args)
    t2 = cv.getTickCount()
    print('Completed in %g seconds'%((t2-t1)/cv.getTickFrequency()))
