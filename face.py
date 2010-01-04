import sys
from opencv import cv

def detect(image, cascade_file='haarcascade_frontalface_alt.xml'):
    image_size = cv.cvGetSize(image)

    # create grayscale version
    grayscale = cv.cvCreateImage(image_size, 8, 1)
    cv.cvCvtColor(image, grayscale, cv.CV_BGR2GRAY)

    # create storage
    storage = cv.cvCreateMemStorage(0)
    cv.cvClearMemStorage(storage)

    # equalize histogram
    cv.cvEqualizeHist(grayscale, grayscale)

    # detect objects
    cascade = cv.cvLoadHaarClassifierCascade(cascade_file, cv.cvSize(1,1))
    faces = cv.cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, cv.cvSize(50, 50))

    if faces:
        for i in faces:
            cv.cvRectangle(image, cv.cvPoint( int(i.x), int(i.y)),
                         cv.cvPoint(int(i.x + i.width), int(i.y + i.height)),
                         cv.CV_RGB(0, 255, 0), 3, 8, 0)
    return faces

