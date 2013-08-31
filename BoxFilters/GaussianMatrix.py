from math import *

def calculate(radius, sigma):
    width = radius+2
    mean = width/2
    Matrix = [[0 for x in xrange(width)] for x in xrange(width)]
    Total = 0
    # generate kernal
    for y in range (0,width):
        for x in range(0,width):
            Matrix[x][y] = exp(-0.5*(pow((x-mean)/sigma,2.0)+(pow((y-mean)/sigma,2.0))))/(2*pi*sigma*sigma)
            Total += Matrix[x][y]
    # normalize
    for y in range (0,width):
        for x in range(0,width):
            Matrix[x][y]=Matrix[x][y]/Total
    return Matrix