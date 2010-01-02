#######
#FILE 1: LIBRARY motion.py
#######
# -*- coding: cp1252 -*-
####################################
#MOTION: compare images for change#
####################################
# Copyright (C) 2007 Erol Baykal
# License: GPL
#AUTHOR:
#   Baykal Erol
#   erol@baykal.be
#   baykal.erol@gmail.com
#
#LAST UPDATED 6 SEP 07
#Version: RC1
##################################

#MODULES
########
import Image, ImageDraw, pygame
from math import fabs, sqrt, pi, atan2

#FUNCTIONS
##########

"""
getMotionArray returns an array containing the (pixelwise) X-Y coordinates of the difference between the two compared images
If the two images are identical an empty array will be returned.
"""
def getMotionArray(image1, image2, threshold = 10):
    i1 = image1
    i2 = image2
    #both images need to be the same size in pixels
    if (i1.size[0] != i2.size[0]) or (i1.size[1] != i2.size[1]):
        return 0 #if not, we return 0
    size = i1.size

    imgArr1 = list(i1.getdata())
    imgArr2 = list(i2.getdata())

    t = threshold
    motionarray = [] #2D array to store motion areas

    i=0
    while i < len(imgArr1): #scan through the images
            p1 = imgArr1[i]
            p2 = imgArr2[i]

            if (fabs(p1[0]-p2[0]) > t) or (fabs(p1[1]-p2[1]) > t) or (fabs(p1[2]-p2[2]) > t): #compare each pixel in R,G,B channel
                    y = i/size[0]
                    x = i - y*size[0]
                    motionarray.append((x,y))

            i = i+1
 
    return motionarray

def getMotionArrayRGB(image1, image2, threshold = 10):
    i1 = image1
    i2 = image2
    #both images need to be the same size in pixels
    if (i1.size[0] != i2.size[0]) or (i1.size[1] != i2.size[1]):
        return 0 #if not, we return 0
    size = i1.size

    imgArr1 = list(i1.getdata())
    imgArr2 = list(i2.getdata())

    t = threshold
    motionarray = [] #2D array to store motion areas

    i=0
    while i < len(imgArr1): #scan through the images
            p1 = imgArr1[i]
            p2 = imgArr2[i]

            if (fabs(p1[0]-p2[0]) > t) or (fabs(p1[1]-p2[1]) > t) or (fabs(p1[2]-p2[2]) > t): #compare each pixel in R,G,B channel
                    y = i/size[0]
                    x = i - y*size[0]
                    motionarray.append((x,y,p2))

            i = i+1
 
    return motionarray

"""
getMotionPoint returns the avarage point of all the motion.
It does this by calculating the medial point for a motion array from getMotionArray
To normalise this point divide pX/imageSizeX and pY/imageSizeY
"""
def getMotionPoint(array):
    area = array
    i=0
    pX = 0
    pY = 0
    point=(-1,-1)
    while i < len(area):    
        pX = pX+area[i][0]
        pY = pY+area[i][1]
        i = i+1
    if i > 0:
        point = (float(pX)/i,float(pY)/i)
    return point

def getAvgColor(array):
    area = array
    i=0
    R = 0
    G = 0
    B = 0
    while i < len(area):    
        R = R+area[i][2][0]
        G = G+area[i][2][1]
        B = B+area[i][2][2]
        i = i+1
    if i > 0:
        color = (int(R/i),int(G/i),int(B/i))
    return color
"""
By examining motion points from two consecutive frames we can detect swing motions.
Swing motions occur when there is enough distance between points
"""
def getSwingMotion(point1, point2, treshold=2):
    p1 = point1
    p2 = point2
    #PYTHAGORAS :) A^2 = B^2+C^2
    B = p1[0] - p2[0]
    C = p1[1] - p2[1]
    A = sqrt((B*B)+(C*C))

    if A > treshold:
        magnitude = A
        vector = (B,C) #vector
        heading = atan2(B,C)*180/pi
        return (magnitude,vector,heading)
    else:
        return 0
"""
Splits coordinates into groups, where each group consists of adjecent coordinates
Receives an array of coordinates ([(x,y),(x,y)]) and retuns an array of array of coordinates ([[(x,y),(x,y)],[(x,y),(x,y)]])
"""
def splitGroups(arr):
    arrGroups= []
    while len(arr) > 1:
        temparr=[arr[0]]
        i = 0
        arr.remove(temparr[0]) #bite off the head of the array ^^
        while i < len(temparr):
            t = checkNeighbours(temparr[i], arr)
            if t:
                for co in t:
                    temparr.append(co)
                    arr.remove(co)
            i=i+1
        arrGroups.append(temparr)
    return arrGroups

"""
takes a coordinate and an array of coordinates. If any neighbouring coordinates of the given coordinate are found in the array, they are returned 
"""
def checkNeighbours(co,arr):
    temp = []
    x = co[0]
    y = co[1]
    neighbours = [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
    for i in arr:
        if (i[0],i[1]) in neighbours:
            temp.append(i)
            
    if len(temp) > 0:
        return temp
    else:
        return 0
    
    
#DEPRECATED

def getMotionArrayOLD(image1, image2, threshold = 10):
    i1 = image1
    i2 = image2
    #both images need to be the same size in pixels
    if (i1.size[0] != i2.size[0]) or (i1.size[1] != i2.size[1]):
        return 0 #if not, we return 0
    size = i1.size

    t = threshold
    motionarray = [] #2D array to store motion areas

    i=0
    while i in range(size[1]): #scan through the images
        j=0
        while j in range(size[0]):
            p1 = i1.getpixel((j,i))
            p2 = i2.getpixel((j,i))

            if (fabs(p1[0]-p2[0]) > t) or (fabs(p1[1]-p2[1]) > t) or (fabs(p1[2]-p2[2]) > t): #compare each pixel in R,G,B channel
                    motionarray.append((j,i))

            j = j+1
        i = i+1
 
    return motionarray



def getMotionArrayRGBOLD(image1, image2, treshold = 10):
    i1 = image1
    i2 = image2
    #both images need to be the same size in pixels
    if (i1.size[0] != i2.size[0]) or (i1.size[1] != i2.size[1]):
        return 0 #if not, we return 0
    size = i1.size

    t = treshold
    motionarray = [] #2D array to store motion areas

    i=0
    while i in range(size[1]): #scan through the images
        j=0
        while j in range(size[0]):
            p1 = i1.getpixel((j,i))
            p2 = i2.getpixel((j,i))

            if (fabs(p1[0]-p2[0]) > t) or (fabs(p1[1]-p2[1]) > t) or (fabs(p1[2]-p2[2]) > t): #compare each pixel in R,G,B channel
                    motionarray.append((j,i,p2))#by deducting these values we mirror the coordinates to mimick a mirror-image
                                          #also return p2; the RGB value for the pixel from the second (newer) image
            j = j+1
        i = i+1
 
    return motionarray

def compare(image1, image2, treshold = 10, showPixels=0):

    #showPixels
    #   if 0: returns bunding box ((x1,y1),(x2,y2)) encompassing all motion
    #   if 1: returns motion mask:
    #       white image with same dimensions of supplied images, where motion areas are marked with a color
    #   if 2: returns motion mask:
    #       white image with same dimensions as supplied images, where motion areas are real pixels of supplied images
    #   if 3: returns motion array:
    #       an array of points, each representing an area of motion on the images
    #images need to have same dimensions
    i1 = image1
    i2 = image2
    #if not, we return 0
    if (i1.size[0] != i2.size[0]) or (i1.size[1] != i2.size[1]):
        return 0
    size = i1.size

    t = treshold

    #2D array to store motion areas
    motionarray = []
    
    #new empty image for motionmask, only create if motion mask is needed
    if (showPixels == 1) or (showPixels == 2):
        ni = Image.new("RGB",i1.size,(0,0,0))
        draw = ImageDraw.Draw(ni)
    
    i=0

    #variables for second boundingbox system
    first = 1
    lX = 0
    hX = 0
    lY = 0
    hY = 0
    while i in range(size[1]):
        j=0
        while j in range(size[0]):
            p1 = i1.getpixel((j,i))
            p2 = i2.getpixel((j,i))

            if (fabs(p1[0]-p2[0]) > t) or (fabs(p1[1]-p2[1]) > t) or (fabs(p1[2]-p2[2]) > t):
                if showPixels == 1:              
                    ni.putpixel((j,i),(255,0,0))
                elif showPixels == 2:
                    ni.putpixel((j,i),p2)
                elif showPixels == 3:
                    motionarray.append((j,i))
                else:
                    if first:
                        lX = j
                        lY = i
                        first = 0
                    if j < lX:
                        lX = j
                    if j > hX:
                        hX = j
                    if i < lY:
                        lY = i
                    if i > hY:
                        hY = i
            j = j+1
        i = i+1
 
    area =  ((lX,lY),(hX,hY))

    if showPixels == 1:
        del draw
        return ni
    elif showPixels == 2:
        del draw
        return ni
    elif showPixels == 3:
        return motionarray
    else:
        return area

